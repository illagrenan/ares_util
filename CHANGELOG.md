# CHANGELOG

## 0.3.0 (2024-01-04)
- `ares_util.ares.call_ares`
  - no longer raise `AresNoResponseError`
  - `city_town_part` has been removed from response
  - `zip_code` is now `int` type instead of `str`
