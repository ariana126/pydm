from assertpy.assertpy import assert_that
from pydm import ServiceContainer


class DummyRepository:
    pass

class UseCaseStub:
    def __init__(self, repository: ServiceContainer):
        self.repository = repository

def test_service_container_resolves_service_dependencies_automatically() -> None:
    # arrange

    # act
    desired_service: UseCaseStub = ServiceContainer.get(UseCaseStub)

    # assert
    assert_that(desired_service).is_instance_of(UseCaseStub)
    assert_that(desired_service.repository).is_instance_of(DummyRepository)