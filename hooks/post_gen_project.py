import shutil

consume_http_apis = "{{cookiecutter.consume_http_apis}}"
if consume_http_apis.lower() != "yes":
    shutil.rmtree("./core/clients", ignore_errors=True)
    # shutil.rmtree("./core/test/test_unittest/test_clients", ignore_errors=True)
    # shutil.rmtree("./core/test/test_integration/test_clients", ignore_errors=True)
