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

- **google_search** - built-in google search for project research
- **AgentTools**
- **SubAgents**
- **FunctionTools**


### Work in Progress Tooling
- **sqlite mcp server** - Implementing for storing projects in a structured 
format.

## Workflow

1. **Prompted by User**: If user provides details about what kind of project
wanted, forward that context on onward, regardless, begin to engage *step2*.
2. **Use `ToddleOpsSequence` tool**
3. **Research and Project Synthesizing** Step
    - Parallel research of art and science projects
    - Project Synthesizer combines/picks best project
4. **Quality Assurance**
    - Check for Safety
    - Edit for grammar and clarity
    - Return project in a standard format to `ToddleOpsRoot`
3. **Project Returned to User**: They can ask for more - or with the 
session and memory services - prompt the agent about past projects as well.

## Attachments
Repo: [asenetcky/toddle-ops](https://github.com/asenetcky/toddle-ops)