# 1)
from setuptools import find_packages,setup
from typing import List
# 3)
hyphen_E_dot="-e ."
def get_requirements(file_path:str)->List[str]:
        requirements=[]
        with open(file_path)as file_obj:
              requirements=file_obj.readlines()
              requirements=[line.replace("\n","")for line in requirements]
        #for removing the hypen e dot from the file on reading
        if hyphen_E_dot in requirements:
            requirements.remove(hyphen_E_dot)


        return requirements




# 2)
setup(
    name="ML:project",
    author="KS",
    version='0.0.1',
    package=find_packages(),
    install_requires=get_requirements('requirements.txt')
)

