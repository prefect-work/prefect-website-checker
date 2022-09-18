from flow import website_checker
from prefect.deployments import Deployment
from prefect.filesystems import S3
from prefect.infrastructure import DockerContainer


s3 = S3.load('data-noaa')
docker = DockerContainer.load('prefect-shared-2-3-1')


deployment = Deployment.build_from_flow(
    flow=website_checker,
    name="Website Checker",
    version="3",
    tags=["uptime-check"],
    storage=s3,
    infrastructure=docker,
    path='website_checker'
)
deployment.apply()
