import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="libtrustbridge",
    version="0.0.1",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/trustbridge/libtrustbridge",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "Flask==1.1.2",
        "Flask-Script==2.0.6",
        "py-cid==0.2.1",
        "multihash==0.1.1",
        "minio==4.0.16",
        "sentry-sdk==0.14.3",
        "boto3==1.13.3",
        "pycountry==19.8.18",
        "marshmallow==3.6.0",
        "apispec[yaml,validation]==3.3.1",
        "apispec-webframeworks==0.5.2",
    ],
    extras_require={
        'testing': [
            "pytest==5.4.1",
            "pytest-flask==1.0.0",
            "freezegun==0.3.15",
        ]
    }
)
