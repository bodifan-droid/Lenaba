# Lenaba Architecture

## Vision

AI creates canonical knowledge.

Lenaba compiles content.

## High-Level Architecture

execution_queue
↓
queue_sync
↓
queue_orchestrator
↓
family_script_builder
↓
family_scripts.parquet
↓
Content Compiler
↓
generator_staging
↓
approve_batch
↓
knowledge_cache
↓
execution_engine
↓
names.parquet
↓
Website

## Core Principles

* Family First Architecture
* Knowledge ≠ Content
* Content Compiler
* Queue as Source of Truth
