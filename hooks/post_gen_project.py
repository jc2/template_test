import shutil

consume_http_apis = "{{cookiecutter.consume_http_apis}}"
if consume_http_apis.lower() != "yes":
    shutil.rmtree("./core/clients", ignore_errors=True)
    shutil.rmtree("./core/tests/tests_unittest/test_clients", ignore_errors=True)
    shutil.rmtree("./core/tests/tests_integration/test_clients", ignore_errors=True)
