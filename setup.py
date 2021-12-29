#!/usr/bin/env python3
from setuptools import setup

# skill_id=package_name:SkillClass
PLUGIN_ENTRY_POINT = 'skill-somafm.jarbasai=skill_somafm:SomaFMSkill'

setup(
    # this is the package name that goes on pip
    name='ovos-skill-somafm',
    version='0.0.1',
    description='ovos somafm skill plugin',
    url='https://github.com/JarbasSkills/skill-somafm',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    package_dir={"skill_somafm": ""},
    package_data={'skill_somafm': ['locale/*', 'ui/*', 'res/*']},
    packages=['skill_somafm'],
    include_package_data=True,
    install_requires=["ovos_workshop~=0.0.5a1", "radiosoma"],
    keywords='ovos skill plugin',
    entry_points={'ovos.plugin.skill': PLUGIN_ENTRY_POINT}
)
