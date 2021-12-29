#!/usr/bin/env python3
from setuptools import setup

# skill_id=package_name:SkillClass
PLUGIN_ENTRY_POINT = 'skill-darker-projects.jarbasai=skill_darker_projects:DarkerProjectsSkill'

setup(
    # this is the package name that goes on pip
    name='ovos-skill-darker-projects',
    version='0.0.1',
    description='ovos wayne june lovecraft readings skill plugin',
    url='https://github.com/JarbasSkills/skill-public-domain-cartoons',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    package_dir={"skill_darker_projects": ""},
    package_data={'skill_darker_projects': ['locale/*', 'res/*', 'ui/*']},
    packages=['skill_darker_projects'],
    include_package_data=True,
    install_requires=["ovos_workshop~=0.0.5a1"],
    keywords='ovos skill plugin',
    entry_points={'ovos.plugin.skill': PLUGIN_ENTRY_POINT}
)
