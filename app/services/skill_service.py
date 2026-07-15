from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Skill, Tool
from app.api.schemas import SkillCreate
import uuid

class SkillValidationError(Exception):
    def __init__(self, message: str):
        self.message = message

def _extract_tool_ids(workflow: dict) -> set:
    tool_ids = set()
    def _search(d):
        if isinstance(d, dict):
            for k, v in d.items():
                if k == "tools" and isinstance(v, list):
                    for t in v:
                        tool_ids.add(str(t))
                else:
                    _search(v)
        elif isinstance(d, list):
            for item in d:
                _search(item)
    
    if workflow:
        _search(workflow)
    return tool_ids

async def create_skill_service(request: SkillCreate, db: AsyncSession) -> str:
    workflow_dict = request.workflow.model_dump()
    steps = workflow_dict.get("steps", {})
    valid_step_names = set(steps.keys())
    valid_step_names.add("end")

    required_steps = workflow_dict.get("required") or []
    for r in required_steps:
        if r not in valid_step_names:
            raise SkillValidationError(f"Required step '{r}' is not defined in steps.")

    for step_name, step_data in steps.items():
        if not isinstance(step_data, dict):
            continue
        next_steps = step_data.get("next") or []
        for n in next_steps:
            if n not in valid_step_names:
                raise SkillValidationError(f"Step '{step_name}' has an invalid next edge: '{n}'. It must be a defined step or 'end'.")

    # Validate tools in the workflow
    tool_ids = _extract_tool_ids(workflow_dict)
    if tool_ids:
        result = await db.execute(select(Tool.id).where(Tool.id.in_(tool_ids)))
        existing_tool_ids = set(row[0] for row in result.all())
        
        missing_tools = tool_ids - existing_tool_ids
        if missing_tools:
            raise SkillValidationError(f"The following tool UUIDs in the workflow were not found: {list(missing_tools)}")

    skill_id = request.id or str(uuid.uuid4())
    new_skill = Skill(
        id=skill_id,
        name=request.name,
        description=request.description,
        prompt=request.prompt,
        category=request.category,
        tools=request.tools,
        workflow=workflow_dict
    )
    db.add(new_skill)
    await db.commit()
    await db.refresh(new_skill)
    return new_skill.id
