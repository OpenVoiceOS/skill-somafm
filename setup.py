#!/usr/bin/env python3
import os

from setuptools import setup
from os import path

# skill_id=package_name:SkillClass
PLUGIN_ENTRY_POINT = 'skill-somafm.openvoiceos=skill_somafm:SomaFMSkill'


def get_requirements(requirements_filename: str):
    requirements_file = path.join(path.abspath(path.dirname(__file__)),
                                  requirements_filename)
    with open(requirements_file, 'r', encoding='utf-8') as r:
        requirements = r.readlines()
    requirements = [r.strip() for r in requirements if r.strip()
                    and not r.strip().startswith("#")]
    if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
        print('USING LOOSE REQUIREMENTS!')
        requirements = [r.replace('==', '>=').replace('~=', '>=') for r in requirements]
    return requirements


setup(
    # this is the package name that goes on pip
    name='ovos-skill-somafm',
    version='0.0.1',
    description='ovos somafm skill plugin',
    url='https://github.com/OpenVoiceOS/skill-ovos-somafm',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    package_dir={"skill_somafm": ""},
    package_data={'skill_somafm': ['locale/*', 'ui/*', 'res/*']},
    packages=['skill_somafm'],
    include_package_data=True,
    install_requires=get_requirements("requirements.txt"),
    keywords='ovos skill plugin',
    entry_points={'ovos.plugin.skill': PLUGIN_ENTRY_POINT}
)
