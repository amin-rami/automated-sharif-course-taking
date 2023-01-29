import aiohttp
import asyncio


class Course:
    def __init__(self, course_id, group, units):
        self.course_id = course_id
        self.group = group
        self. units = units
        self.endpoint = 'https://my.edu.sharif.edu/api/reg'
        self.session = None

    async def get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    async def add_course(self, authorization):
        headers = {'Authorization': authorization}
        data = {
            'action': 'add',
            'course': f'{self.course_id}-{self.group}',
            'units': self.units
        }
        session = await self.get_session()
        async with session.post(self.endpoint, json=data, headers=headers) as response:
            print(await response.json())

    async def move_course(self, new_group, authorization):
        headers = {'Authorization': authorization}
        data = {
            'action': 'move',
            'course': f'{self.course_id}-{new_group}',
            'units': self.units
        }
        session = await self.get_session()
        async with session.post(self.endpoint, json=data, headers=headers) as response:
            print(await response.json())
        self.group = new_group


async def main(courses: list[Course], authorization):
    tasks = []
    replication = 20
    for course in courses:
        tasks.extend([course.add_course(authorization) for _ in range(replication)])
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    energy_systems_analysis_data = {
        'course_id': '25753',
        'group': '1',
        'units': 3
    }
    linear_algebra_data = {
        'course_id': '25872',
        'group': '2',
        'units': 2
    }
    authorization = 'TO-BE-DETERMIND'

    energy_systems_analysis = Course(**energy_systems_analysis_data)
    linear_algebra = Course(**linear_algebra_data)
    courses = [energy_systems_analysis, linear_algebra]

    asyncio.run(main(courses, authorization))
    for course in courses:
        course.session.close()
