from setuptools import setup

package_name = 'my_chess_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ekambehl',
    maintainer_email='ekambehl@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_listner=my_chess_controller.depth_sub:main',
            'board_state=my_chess_controller.board_state:main',
            'red_pieces=my_chess_controller.chess_pieces:main',
            'blue_pieces =my_chess_controller.blue_chess:main',
            'key_board=my_chess_controller.keyBoard:main'
        ],
    },
)
