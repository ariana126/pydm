from assertpy.assertpy import assert_that
from pydm import ServiceContainer

class DummyUnitOfWork:
    pass
class RepositoryStub:
    def __init__(self, unit_of_work: DummyUnitOfWork):
        self.unit_of_work = unit_of_work
class UseCaseStub:
    def __init__(self, repository: RepositoryStub):
        self.repository = repository


def test_only_one_instance_of_service_container_exists() -> None:
    # arrange
    sut: ServiceContainer = ServiceContainer.get_instance()

    # act
    instance2: ServiceContainer = ServiceContainer.get_instance()
    instance3: ServiceContainer = ServiceContainer()

    # assert
    assert_that(instance2).is_equal_to(sut)
    assert_that(instance3).is_equal_to(sut)

def test_service_container_resolves_service_dependencies_automatically() -> None:
    # arrange
    sut: ServiceContainer = ServiceContainer.get_instance()

    # act
    desired_service: UseCaseStub = sut.get_service(UseCaseStub)

    # assert
    assert_that(desired_service).is_instance_of(UseCaseStub)
    assert_that(desired_service.repository).is_instance_of(RepositoryStub)
    assert_that(desired_service.repository.unit_of_work).is_instance_of(DummyUnitOfWork)