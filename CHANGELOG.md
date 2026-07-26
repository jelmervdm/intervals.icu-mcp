# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-07-26

### Fixed
- Redirected container entrypoint `echo` startup messages to `stderr` (`>&2`). Prevents non-JSON-RPC output on `stdout` which caused stdio MCP clients (such as Antigravity) to fail initialization with `invalid character 'S' looking for beginning of value`.

## [0.1.0] - 2026-07-26

### Added
- Initial release of `intervals-icu-mcp-server`.
- Full Intervals.icu REST API integration (`IntervalsClient`).
- Support for Athlete profile retrieval (`get_athlete_profile`).
- Activity management tools: list, fetch, update, delete, and comments.
- Calendar & Planned Workout event management tools: list, fetch, create, update, delete.
- Wellness tracking tools: list, fetch, and update daily metrics.
- Workout library tools: list folders and structured workouts.
- Semantic tool routing integration via `fastembed` (`TOOL_ROUTING=true`).
- Native IBM ContextForge Gateway support (`ENABLE_CONTEXTFORGE_GATEWAY=true`).
- Docker container deployment and GitHub Actions workflows.
