# Revision of TikTok

This paper was previously submitted to the fall deadline of Oakland '21 and
received a major revision in December 2020. Since then, we have fundamentally
reworked the design to address the underlying issues that were pointed out by
the reviews.

The two key weaknesses, as observed by the Oakland reviewers, were the inherent
deadlock proneness and the lack of clarity regarding whitelisting of system
calls.

Overall, in this revision we have

* clarified, extended, and systematized the attacks
* clarified and rewritten the design and implementation
* reengineered the TikTok design to remove deadlocks
* extended the evaluation

We provide more details on deadlock freedom and whitelisting, as requested by
the reviewers below.


## Deadlock freedom in revision

We have addressed the first by redesigning TikTok along our newly introduced
core invariant of ensuring that each address that is read during the execution
of a system call remains constant across multiple reads. We have drawn
inspiration from database design and transactional memory systems that had to
solve similar challenges. 

Our new design is now inherently deadlock free *by design*. 


## Whitelisting of system calls

We clarify why certain system calls (such as `futex`) need to be excluded from
TikTok protection and define what these system calls are. We argue why the set
of described system calls is sufficient and how they are determined---through
careful analysis and reasoning about the different system calls. This (small)
set is experimentally confirmed and we do not experience any issues with the
execution of our broad benchmark sets.


## Why Usenix SEC and not Oakland?

The redesign of TikTok took overall 8 months of heavy engineering and design
work across multiple people. Our goal was to fix the underlying issues even if
it meant that we missed the major revision deadline. We are now satisfied with
the new version and experiments and therefore submit our revised paper to Usenix
Security.


## Revision

We are attaching the unaltered and complete Oakland'21 reviews, the original
paper, and the latexdiff to this document.
