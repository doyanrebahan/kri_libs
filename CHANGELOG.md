# Changelog

<!--next-version-placeholder-->

## v0.1.0 (25/08/2022)

- First release of `kri_lib`!

## v0.2.0 (10/10/2022)

- Add lazy db connection class.
- Add pymongo as required installation.
- Add logging:
  - with django built in handler ``logging``
  - implemented API_ID as identifier for each service.
  - new requests utils to add API_ID as default header.
  - with django middleware
  - stored in mongodb
  - slack notification integrations