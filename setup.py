from setuptools import setup

setup(
    name='skillcorner',
    version='1.0.6',
    description='SkillCorner API client',
    long_description='SkillCorner API client used to get endpoint data',
    author='SkillCorner',
    author_email='support@skillcorner.com',
    packages=['skillcorner'],
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.20.0',
        'makefun>=1.10.0'
    ],
    extras_require={
        'test': 'mock==4.0.3',
        'release': ['Sphinx==4.2.0', 'sphinx-rtd-theme==1.0.0']
    }
)
