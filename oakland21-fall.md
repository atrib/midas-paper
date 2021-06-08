IEEE S&P 2021 Paper #303 Reviews and Comments
===========================================================================
Paper #303 TikTok: Kernel TOCTTOU Protection


Review #303A
===========================================================================

Overall merit
-------------
3. Weak accept - While flawed, the paper has merit and we should consider
   accepting it.

Reviewer expertise
------------------
2. Some familiarity - I know some basics about the area, have seen talks,
   skimmed papers, etc.

Reviewer confidence
-------------------
2. Medium

Paper summary
-------------
This paper aims to protect the kernel from double-fetch bugs without requiring
the program source code, with a framework called TikTok. TikTok system aims to
mitigate double-fetches by enforcing the protecting pages to be changed only
when allowed and intended. TikTok’s core logics are implemented in a modified
system call, which copies the kernel page to the user and page-fault handler.

Strengths
---------
+ A novelty in terms of not requiring source code of the subject system call. It
can work on binary.
+ Generally good performance.

Weaknesses
----------
- High overhead on programs with heavy multithreading
- Not all system calls are perfectly protected.

Detailed comments for authors
-----------------------------
Compared to prior works such as DFTinker [1], this paper is novel because this
work does not require the source code of the problematic program. As far as my
knowledge goes, I could not find a similar work that does the same to a binary,
rather than a source code.

The paper’s motivation mentions binary-only codes such as external drivers, and
many vital functions are not system calls such as file system handlers. Can they
be handled in the same way as implemented in this paper?

In section V-D, it says to prevent deadlocks, all locks are taken in increasing
order but the two locks; page-table lock and interval-tree lock. Does the order
matter to avoid deadlocks? Could you elaborate on how? How many locks are there,
and which kinds? Is the page-table lock global (i.e., already in the kernel), or
just in TikTok? If the latter, what happens if an adversary tries to change the
permission of the page table via system call while the page-table lock is held?

I wish there were a security evaluation where a few CVEs are tested to prove
that TikTok is effective to those CVEs.



Typo
- “marked memory memory ranges” on page 4 (is it intentional?)
- "through through" (should be one through) on page 1
- whitelisting.. (should be one period) on page 4
- "It is already mapped an can be edited" (should be "and") on page 5
- "unused bis" (should be "unused bits") on page 6
- "TikTok extends copy_to_user to mark the pages" (should be "copy_from_user")
  on page 6
- "when marking a page the page-table lock needs to be acquired ﬁrst" (should
  contain a comma) on page 7
- "Table ??" on page 10

[1] DFTinker: Detecting and Fixing Double-Fetch Bugs in an Automated Way



Review #303B
===========================================================================

Overall merit
-------------
2. Weak reject - The paper has flaws, but I will not argue against it.

Reviewer expertise
------------------
2. Some familiarity - I know some basics about the area, have seen talks,
   skimmed papers, etc.

Reviewer confidence
-------------------
2. Medium

Paper summary
-------------
TIKTOK presents a new kernel defense for preventing the exploitation
of latent double-fetch bugs in syscalls. TIKTOK accomplishes this via
first marking all pages read by syscalls as read-only, and then by
careful management of all future writes and page mappings to prevent
issues. The paper includes a detailed performance evaluation against
benchmarks and real programs likely to be affected by the defense.

Strengths
---------
 + Defense objectives and limitations are well defined
 + Excellent performance evaluation benchmarking

Weaknesses
----------
 - Inherent deadlocks and unexpected userspace behaviors in design
 - Unclear benefits to whitelisting approach

Detailed comments for authors
-----------------------------
There are several design challenges that TIKTOK needs to either
address or discuss at more length.

Most pressingly, TIKTOK introduces deadlocks where none existed
previously(S IV.C). While this is discussed in the paper, it is not
sufficient to declare them 'unlikely in practice'. TIKTOK can break
legal program behavior in a non-obvious way and does not have a
recovery mechanism if this happens. This is in contrast to most
systems defensive schemes (e.g. stack canaries, ASLR, flushing buffers
on context switch, guard pages, etc) that may break illegal program
behavior, but not legal programs. As with the fixed kernel deadlock
case (S V.D), TIKTOK would need to address this possibility and
provide recovery that matches existing syscall semantics.

The discussion around syscall 'whitelisting' is somewhat confusing and
it is not clear how this would be viable in practice. First, I don't
see why disabling marking for mmap or munmap would cause any behavior
differences if they already didn't perform any reads, I assume no
userspace reads always results in no marking overhead. Second, any
syscall in the whitelist must be constantly re-verified to be
exploit-free, not just once upon initial deployment of the
defense. This would imply that we have the ability to regularly check
and fix syscalls that perform double-fetches, at which point we can
apply this methodology more widely and no longer need TIKTOK. TIKTOK
is at its best argument for a security benefit when it can simply be
'on' all the time.

There is also a more subtle breakage around the copy_to_user
behavior. Any write that crosses page boundaries may 'partially'
commit, which may lead to unexpected userland behavior. Example: Write
crosses pages p1 p2, p1 is marked, p2 is not. P1 write is deferred, P2
is present and write commits. Some portion of the result is now
written (the portion in p2) and the total write may hang for an
arbitrarily long time. This doesn't obviously break most programs, but
it is odd.

It was not clear why the page-fault handler must wait for the page to
become unmarked before returning. Why can it not create a deferred
write as it would have if the page were marked and present?

Minor:
 - S VI.C "Table ??" missing ref
 - What types of locks are being used?
 - How are deferred writes finalized?

Requested changes
-----------------
 - Avoid deadlocking otherwise valid programs

 - Explain how to run the whitelisting model in practice (and over
   time)



Review #303C
===========================================================================

Overall merit
-------------
3. Weak accept - While flawed, the paper has merit and we should consider
   accepting it.

Reviewer expertise
------------------
3. Knowledgeable - I know the area well (key related work is quite familiar
   to me).

Reviewer confidence
-------------------
2. Medium

Paper summary
-------------
TikTok is a double fetch mitigation protecting the linux syscalls against the
exploitation of double fetch bugs. First, it finds a page frame number (PFN)
that matches a pointer provided to copy_from_user(). Second, it finds all page
table entries that reference this PFN and set these to read-only before it
allows copy_from_user to read the actual data. The page table entries are reset
when the syscall returns. This makes sure that an attacker cannot modify memory
already read by the syscall thus making it safe to double fetch. Other threads
are stalled when the page fault triggers.

Strengths
---------
+ Interesting idea

Weaknesses
----------
+ The paper could use some proof reading

Detailed comments for authors
-----------------------------
The paper could use with some proof reading. For example: “Storing arguments on
such pages can result in reading different values from them, even if no writes
occur inbetween the reads.”  It’s unclear what “such pages” refer to (inbetween
is 2 words). “Table ??” in reference to table 2 in another example 
I like the systematization of different types of double fetch conditions for
syscalls under Linux at it is important to explicitly state what you wish to
protect against and it’s nice to see the attack number 5 mentioned and  fair
that it’s caveated out with DAC. 
One thing I didn’t notice in the paper is what would happen if a malicious user
called mprotect. From figure 4 there appears to be no lock preventing using
mprotect from modifying permissions between two calls to copy_from_user.  This
is surely a solvable problem, but a discussion would benefit the paper. 
It would’ve been great if the evaluation had occupied itself with how often
marking a page leads to a waiting writes. It’s easy to imagine blocks that takes
a significant amount of time – e.g. because the system call reads from rotary or
remote media or before returning. Also, the breakdown of where the performance
penalties occurs would be useful to see how the solution scales with more cores,
and different workloads not considered in the evaluation.
White lists are great, but they do beg the question on how they are made. If we
can detect double fetch bugs reliably fixing them seems to be the better
solution given there is a performance penalty for TikTok. If we can’t, TikTok
because a attack surface reduction method with arbitrary selection of attack
surface.
Windows has a mode for drivers where ioctl input data copied to a immutable
mapping by the kernel before it is provided to the drivers. It is deallocated on
finishing the ioctl. This effectively prevent double fetch bugs in a different
way, but only for ioctl input. A similar approach could be implemented as an
alternative copy_from_user. I mention this as a potential avenue for future
research or as an alternative to blocking.

Nitpicks:
“So far, the only protection against double-fetch bugs is to detect and fix
them.” This statement seems to be contradicted by the discussion of DropIt later
in the paper. Qualifying the statement would make it correct as DropIt has a
significant number of caveats.
“Double-fetches introduced by the compiler are another challenge. While the
source code and even the intermediate representation may be bug free, the
compiler can introduce such “invisible” double-fetches when allocating registers
to variables. TikTok protects the system against all kinds of double fetches.
representation may be bug free, the compiler can introduce such “invisible”
double-fetches when allocating registers to variables.
Figure 4 – the bold writing hardly comes across. Maybe marking new steps with
color?

Requested changes
-----------------
- I'd like to see a break down of where the penalties comes from to allow
  extrapolation of penalties to other scenarios and hardware.
-



Review #303D
===========================================================================

Overall merit
-------------
3. Weak accept - While flawed, the paper has merit and we should consider
   accepting it.

Reviewer expertise
------------------
3. Knowledgeable - I know the area well (key related work is quite familiar
   to me).

Reviewer confidence
-------------------
2. Medium

Paper summary
-------------
This paper provides a new solution to the problem of double-fetch bugs in the
Linux kernel. During a system call, the solution essentially marks any page read
from userspace as read-only as soon as it is read, and defers any further writes
to the page until the system call finishes. Although this is conceptually
simple, there is a lot more work required to ensure that pausing thread that
want to write doesn't cause deadlocks in the kernel. The authors implement the
system for the Linux kernel on x86 and show that its overhead is generally low
(~17% when applied to all system calls, and less when some system calls are
whitelisted).

Strengths
---------
+ Very low overhead, particularly when a handful of manually-audited system
calls can be excluded
+ Simple solution that can be applied on many different architectures

Weaknesses
----------
- No security evaluation of the solution, just performance measurement

Detailed comments for authors
-----------------------------
This paper provides a well-engineered, carefully thought out solution to TOCTTOU
(aka double-fetch bugs). The basic idea is very intuitive, but the authors do a
good job showing that avoiding deadlocks requires a lot of careful thought.

One thing that seems to be missing is an evaluation of the security of this
solution, e.g. by showing that previously exploitable double-fetch bugs become
exploitable, or by demonstrating that the correctness argument is sound. Right
now it seems like the correctness argument relies on the authors having
exhaustively enumerated all the ways a memory page can change in between two
reads. I'm not totally convinced that the list given is exhaustive—it would be
helpful if the authors could clarify how they came up with the list, and how
they know it covers everything?

Given that there is still some performance overhead from this solution, it would
be great if the authors could mention whether this can also be used for
double-fetch detection (as in DECAF). Ideally, one could use this system as a
stopgap while double-fetch bugs are found and fixed, and perhaps eventually
disable it (or progressively whitelist more and more system calls, improving
performance).

Since this appears to be an effort to create a production-ready system, have the
authors made efforts to get this integrated into the Linux kernel?

Minor:

* Is it guaranteed that all accesses to user memory will go through
* copy_from_user? I know that this is the (strong) recommendation, but given
* that user memory is still directly accessible from kernel space (at least on
* x86), could there be any code that does direct dereference?

* A little more explanation of the system call wrapper problem would be helpful.
* I think I get what the problem is (a wrapper may need to fetch information
* that is then re-fetched by the original call), but an example would be useful.



Comment @A1
---------------------------------------------------------------------------
This paper was discussed by the PC and the decision was to offer it the option
to resubmit a revision. The main revision requirements the PC would like to see
addressed are: 

- Demonstrate what realistic cases cause deadlocks and a mechanism to avoid
  them.
- Explain how to deploy whitelisting of syscalls in an efficient and productive
  way.
- Address other comments from reviews.

Your PC point of contact is David Kohlbrenner <david.kohlbrenner@gmail.com> in
case you have any questions about the revision.

