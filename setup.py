from setuptools import setup

__version__ = (0, 0, 0)

setup(
    name="sea_ice_phenology",
    description="Sea Ice Phenology Indicator Extraction from Remote Sensing Data",
    url="https://github.com/sum1lim/rs_tools",
    version=".".join(str(d) for d in __version__),
    author="Sangwon Lim",
    author_email="sangwonl@uvic.ca",
    packages=["sea_ice_phenology"],
    include_package_data=True,
    scripts="""
        ./scripts/gui
        ./scripts/authenticate
        ./scripts/get_timeseries
        ./scripts/interpolate
        ./scripts/phenology
    """.split(),
)
