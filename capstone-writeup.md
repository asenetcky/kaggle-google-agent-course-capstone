# Kaggle x Google 5-day AI Agents Intensive Course Capstone

## Basic Details
 
 
Title: **ToddleOps Project Generation Agent**
Subtitle: *Project Generation for Exhausted Parents and Caregivers of Toddlers*

Card and Thumbnail Image: [toddle-ops](images/toddle-ops.png)

## Submission Tracks

Track: Concierge Agents

## Project Description

> Max 1500 words

Keeping a toddler happily occupied is a fulltime job, and the odds are, you 
already have a fulltime job. Sprinkle in some sleep depravation, and your
little one is likely to miss out on enriching activities.

> Enter ToddleOps Project Generation Agent

Lower the barrier of entry to safe, fun toddler activities to the absolute
floor with the ToddleOps Agent. It will provide projects, in a standard,
easy to follow format so *all* you have to do is conjure up every last drop
of willpower in your tired, aching body to actually *do* the project!

## Agent Architecture

### Main Agent: ToddleOpsRoot

The main agent is a `LlmAgent` called `ToddleOpsRoot` using 
`gemini-2.5-flash-lite` and is housed inside of an `App()` with event
compaction, a local `DatabaseSessionService` and `MemoryService` with
preload.

### Sub Agents

`ToddleOpsRoot` uses a `SequentialAgent` as an `AgentTool` called 
`ToddleOpsSequence`.

`ToddleOpsSequence` has two parts to the sequence.

    1. A *Craft Reseearch Team* made up of the following wrapped in its own
    `SequentialAgent`
        - `ParallelAgent` team that researches toddler projects
        - `LlmAgent` That picks the best project, and/or combines the projects
        in novel ways.
    2. A *Quality Assurance Team* that that is a `SequentialAgent` composed of
    the following:
        - `LoopAgent` checking projects for safety, providing feedback and
        approving projects when they are deemed sage
        - `LlmAgent` acting as an editor checking grammar and clarity.

## Tools



workflow

## Attachments

links to code etc...
