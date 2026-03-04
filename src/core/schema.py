from pydantic import BaseModel, Field


class Socials(BaseModel):
    github: str = ""
    linkedin: str = ""
    email: str = ""
    twitter: str = ""


class SkillTiers(BaseModel):
    tier1: list[str] = Field(default_factory=list)
    tier2: list[str] = Field(default_factory=list)
    tier3: list[str] = Field(default_factory=list)


class Project(BaseModel):
    name: str = ""
    description: str = ""
    tech: list[str] = Field(default_factory=list)
    demo_url: str = ""


class BackgroundEntry(BaseModel):
    icon: str = "🔹"
    label: str = ""
    value: str = ""


class ProfileConfig(BaseModel):
    name: str = ""
    github_username: str = ""
    taglines: list[str] = Field(default_factory=list)
    about: str = ""
    socials: Socials = Field(default_factory=Socials)
    skills: SkillTiers = Field(default_factory=SkillTiers)
    projects: list[Project] = Field(default_factory=list)
    background: list[BackgroundEntry] = Field(default_factory=list)
    theme: str = "developer"
    footer_text: str = "Built with curiosity. Updated with intent."
    sections: list[str] = Field(
        default_factory=lambda: [
            "header", "about", "skills", "projects", "background", "footer"
        ]
    )
