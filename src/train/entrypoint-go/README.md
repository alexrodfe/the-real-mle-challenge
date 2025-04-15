# REST trigger

The REST webhook trigger is a predefined KAI process that creates a REST server instance.  
It will stay listening for client requests through port 8080.  

## How to setup

There is an optional "path" configuration for users to specify the path in which the REST service will be deployed.
If no "path" is setup, the trigger will be in the default "trigger" path.

Processes communicating with this trigger must be prepared to do so. Processes listening to
the REST trigger need to unmmarshal protobuf based JSON messages, and processes sending messages to
the trigger need to marshal protobuf based JSON messages.

Both output and input messages towards this process require the usage of specific keys in the JSON.

### Configuration

The configuration should be defined inside the `centralized configuration scope`:

| Key       | Optional  | Type | Value                                                                                         |
|-----------|-----------|------|----------------------------------------------------------------|
| path      | yes       | str  | Where the REST service will be deployed ("trigger" by default).     |

#### Configuration Example

```yaml
centralized_configuration:
  process:
    config:
      path: 'mypath'
```

### Trigger's Output (JSON)

| Key       | Type    | Value                                                                                     |
|-----------|---------|-------------------------------------------------------------------------------------------|
| method    | str     | The REST method used                                                                      |
| body      | []byte  | Optional. For POST and PUT methods the body is taken from the request's body              |

#### Trigger's Output Example

```json
{
 "method": "POST",
 "body": {"keyA": "valueA", "keyB": "valueB"},
}
```

### Trigger's Input from other processes (JSON)

| Key         | Type | Value                                                                      |
|-------------|------|----------------------------------------------------------------------------|
| status_code | str  | Status code for the workflow execution, used later in http server response |
| message     | str  | A message sent by the user                                                 |

#### Trigger's Input Example

```json
{
 "status_code": "200",
 "message": "All good!",
}
```

### Trigger's Output to client (JSON)

| Key       | Type | Value                                                                  |
|-----------|------|------------------------------------------------------------------------|
| message   | str  | A message                                                              |

#### Trigger's Output to client

```json
{
 "message": "All good!",
}
```
