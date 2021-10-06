from distutils.core import setup

setup(
 name='ac2imp',
 author = "Qiang Lu modified Dennis Muhlestein's csv2ofx",
 version='0.1',
 packages=['ac2imp'],
 package_dir={'ac2imp':'src/ac2imp'},
 scripts=['ac2imp'],
 package_data={'ac2imp':['*.xrc']}
)

