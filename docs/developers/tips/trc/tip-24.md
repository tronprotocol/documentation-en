---
author: '@shydesky <shydesky@gmail.com>'
category: TRC
created: '2019-03-04'
discussions to: https://github.com/tronprotocol/tips/issues/24
status: Final
tags:
- Final
- TRC
tip: '24'
title: Implement DB storage with RocksDB
type: Standards Track
---

## Simple Summary

Implement the database storage layer with RocksDB.

## Abstract

Currently, the java-Tron project uses LevelDB as the only implement of the database storage layer. This Tip is created for the purpose of adding a new implementation of the database storage layer.

## Motivation

RocksDB is a good storage engine built on earlier work on LevelDB and it is widely used in production environments. It has higher performance when storing key-value data benefiting from exploiting many CPU cores than LevelDB.RocksDB provides all of the features of LevelDB and some useful functions like backups and snapshots. It is very friendly to the developers to find the bottleneck of the system and contains many parameters used to tune RocksDB for your workload and your system configuration.
So, it wisely adds the implementation of the database storage layer with RocksDB to make our java-Tron more effective and robust.

## Copyright

Copyright and related rights waived via [CC0](https://github.com/tronprotocol/tips/blob/master/LICENSE.md).