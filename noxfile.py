import nox


@nox.session
def tests(session):
    session.install("-r", "requirements-dev.txt")
    session.install("-e", ".")
    session.run("pytest", "-q")


@nox.session
def type(session):
    session.install("mypy")
    session.run("mypy", "src")


@nox.session
def lint(session):
    session.install("black")
    session.run("black", "--check", ".")
