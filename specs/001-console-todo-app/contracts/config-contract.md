# Configuration Contract - Console Todo App

## Overview
This document defines the configuration contract for the Console Todo Application, specifying the expected configuration structure, validation rules, and behavior.

## Configuration Sources Hierarchy

The application follows this hierarchy for configuration sources (in order of precedence):
1. **Command-line arguments** - Highest precedence
2. **Environment variables** - Medium precedence
3. **User configuration file** - Low precedence, default values
4. **Built-in defaults** - Lowest precedence

## Configuration File Location

### Default Locations by Platform
- **Unix/Linux/macOS**: `~/.config/todo_app/config.json`
- **Windows**: `%APPDATA%\todo_app\config.json`

### Overridable Location
- Can be specified via `TODO_CONFIG_PATH` environment variable
- Can be specified via `--config` command-line argument

## Configuration Schema

### Root Level Properties

```json
{
  "storage": {
    "path": "string",
    "format": "string",
    "backup_enabled": "boolean",
    "backup_count": "integer"
  },
  "display": {
    "date_format": "string",
    "show_completed": "boolean",
    "color_enabled": "boolean",
    "theme": "string",
    "priority_colors": {
      "low": "string",
      "medium": "string",
      "high": "string"
    }
  },
  "defaults": {
    "priority": "string",
    "auto_archive": "boolean",
    "confirm_deletion": "boolean"
  },
  "behavior": {
    "auto_save": "boolean",
    "case_sensitive_search": "boolean",
    "fuzzy_matching": "boolean"
  }
}
```

### Detailed Property Definitions

#### Storage Configuration
- **path** (string, optional)
  - Default: `~/.todo_app/todos.json`
  - Description: Path to the todo storage file
  - Validation: Must be a valid file path with write permissions

- **format** (string, optional)
  - Default: `"json"`
  - Valid values: `"json"`, `"yaml"`, `"csv"`
  - Description: Storage format for todo data

- **backup_enabled** (boolean, optional)
  - Default: `true`
  - Description: Whether to create backups before write operations

- **backup_count** (integer, optional)
  - Default: `5`
  - Minimum value: `1`, Maximum value: `10`
  - Description: Number of backup files to maintain

#### Display Configuration
- **date_format** (string, optional)
  - Default: `"YYYY-MM-DD"`
  - Description: Format string for displaying dates
  - Valid formats: ISO 8601 compatible formats

- **show_completed** (boolean, optional)
  - Default: `true`
  - Description: Whether to show completed todos by default

- **color_enabled** (boolean, optional)
  - Default: `true`
  - Description: Enable colored output in terminal

- **theme** (string, optional)
  - Default: `"default"`
  - Valid values: `"default"`, `"dark"`, `"light"`, `"high-contrast"`
  - Description: Color theme for terminal output

- **priority_colors** (object, optional)
  - Description: Color mapping for priority levels
  - Properties:
    - **low** (string, optional) - Default: `"green"`
    - **medium** (string, optional) - Default: `"yellow"`
    - **high** (string, optional) - Default: `"red"`

#### Defaults Configuration
- **priority** (string, optional)
  - Default: `"medium"`
  - Valid values: `"low"`, `"medium"`, `"high"`
  - Description: Default priority for new todos

- **auto_archive** (boolean, optional)
  - Default: `false`
  - Description: Automatically archive completed todos

- **confirm_deletion** (boolean, optional)
  - Default: `true`
  - Description: Prompt for confirmation before deleting todos

#### Behavior Configuration
- **auto_save** (boolean, optional)
  - Default: `true`
  - Description: Automatically save changes to storage

- **case_sensitive_search** (boolean, optional)
  - Default: `false`
  - Description: Whether search is case sensitive

- **fuzzy_matching** (boolean, optional)
  - Default: `true`
  - Description: Enable fuzzy string matching for search

## Environment Variables

### Direct Mapping
- `TODO_STORAGE_PATH` → `storage.path`
- `TODO_DATE_FORMAT` → `display.date_format`
- `TODO_SHOW_COMPLETED` → `display.show_completed`
- `TODO_COLOR_ENABLED` → `display.color_enabled`
- `TODO_DEFAULT_PRIORITY` → `defaults.priority`
- `TODO_CONFIRM_DELETION` → `defaults.confirm_deletion`
- `TODO_AUTO_SAVE` → `behavior.auto_save`

### Type Conversion for Environment Variables
- String values "true"/"false" convert to boolean
- Numeric strings convert to integers where applicable
- Case-insensitive for boolean values

## Validation Rules

### Required Format
- Configuration file must be valid JSON
- Root object must be a JSON object
- Property names must match the defined schema

### Value Constraints
- Date format strings must be valid ISO 8601 patterns
- File paths must be writable
- Backup count must be between 1 and 10
- Priority values must be one of the allowed values

### Validation Behavior
- Invalid configuration values should fall back to defaults
- Missing properties should use default values
- Invalid configuration files should log errors but not crash the application

## Backward Compatibility

### Versioning
- Configuration schema follows semantic versioning
- Major version changes may introduce breaking changes
- Minor version changes add optional properties only

### Migration
- Support for older configuration formats where possible
- Automatic migration of configuration files when possible
- Clear error messages for unsupported configuration versions

## Error Handling

### Invalid Configuration
- Log configuration errors to stderr
- Use sensible defaults when values are invalid
- Continue operation with partial configuration

### Missing Configuration File
- Create default configuration file if none exists
- Place default file in the appropriate platform-specific location

### Permission Errors
- Log permission errors
- Fall back to in-memory configuration if file is not writable
- Warn user about data persistence issues

## Default Configuration

```json
{
  "storage": {
    "path": "~/.todo_app/todos.json",
    "format": "json",
    "backup_enabled": true,
    "backup_count": 5
  },
  "display": {
    "date_format": "YYYY-MM-DD",
    "show_completed": true,
    "color_enabled": true,
    "theme": "default",
    "priority_colors": {
      "low": "green",
      "medium": "yellow",
      "high": "red"
    }
  },
  "defaults": {
    "priority": "medium",
    "auto_archive": false,
    "confirm_deletion": true
  },
  "behavior": {
    "auto_save": true,
    "case_sensitive_search": false,
    "fuzzy_matching": true
  }
}
```

## Extensibility

### Future Properties
- New properties should be optional with sensible defaults
- Add properties to the appropriate configuration section
- Maintain clear separation between storage, display, defaults, and behavior

### Custom Configuration
- Applications may extend configuration with custom properties
- Custom properties should be prefixed to avoid conflicts
- Custom properties should be documented in implementation-specific docs