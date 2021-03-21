#automation-lambda

## Contents

- start_tagged_instances.py
- stop_tagged_instances.py

## Usage

### Lambda Setting

Remember to increase the following two values from default

- Timeout: 10 minutes
- Memory: 512 MB

The actual value to set depends on how many instances you have.
The above value is just a safe estimation.

### Environment Variables

- region: the region where the tagged EC2s are located
- tags: the tags on the target EC2 in JSON format (Can Enter Multiple tags. Will only start/stop instances that match all the tags)

### Testing

If you want to test what instances will be started/stopped without actually performing the action, you can comment out everything after line 41 (after the comment  "Start/Stop All Found Instances") for that.
