# ylog
ylog is a versitile yet minimalistic Python logging client for cloud and 
on-prem environments.

Motivation for ylog's existence is that, even as surprising as it may sound,
lack of an efficient yet versitile enough logging client to be reused between
different projects and hosting enviroments.
In 2020. Hence the name, yolo logging. 

## Getting started
*Project is not ready for use, still work in progress*

Install with pip:
```
pip install ylog
```

Example usage:
```
import ylog

log = ylog.Log()
log.debug('debug msg')
log.info('info msg')
log.warn('warning msg')
log.error('error msg')
```

By default, ylog outputs to `stdout`.

## Goals
1. Minimalistic, no dependencies
2. Performant, non-blocking I/O
3. Versatile, support on-prem as well as cloud applications (such as AWS
   Lambda, GCP Cloud Functions, etc)

## Contributing
This project accepts contributions via GitHub pull requests. Please check issues
first to make sure no one else is working on the same thing.

## License
ylog is under the LGPL 3.0 license. See the [LICENSE](LICENSE) file for details.
