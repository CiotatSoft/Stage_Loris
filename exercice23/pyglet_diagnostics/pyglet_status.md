Looks like you did a nice job on the fix, congratulations !!


I retrieved the `exercise23` file, and `valgrind` finds a lot less errors. All `invalid read memory accesses` that were present during the textureCreation are not present anymore, so, even if i had no segfault on my PC, now, valgrind is happy, so am i :)

------
There are however still some errors remaining.

------

The most obvious one is that where the `exercise23` plays a sound, the `close()` system call is given an `invalid file_descriptor` many time (something like 15 times for 1 sound).
 This usually happens when you do something like:
```python
file_descriptor = open("blabla")
close(file_descriptor)
close(file_descriptor) # <---- second time closed should not happen
```
It may also happen if the open of a file_descriptor fails, and you close it. In order to ensure the case, i'll make a python script to parse the output of `strace python3 exercise23.py` and track the open/close file descriptors. i don't have the time right now.
But you can find the logs of strace in the file `strace.log`

Action i must do for you
   - [] track the file descriptors
   - [] find the origin of these many unnecessary close() calls

------


The most important `valgrind`'s report  is a read of uninitialized memory: here is a copy paste of that issue from `valgrind`'s point of view

```log
==60268== Invalid read of size 8
==60268==    at 0x40286C8: strncmp (strcmp.S:172)
==60268==    by 0x400668D: is_dst (dl-load.c:216)
==60268==    by 0x400810E: _dl_dst_count (dl-load.c:253)
==60268==    by 0x400810E: expand_dynamic_string_token (dl-load.c:395)
==60268==    by 0x40082B7: fillin_rpath.isra.0 (dl-load.c:483)
==60268==    by 0x4008602: decompose_rpath (dl-load.c:654)
==60268==    by 0x400ABF5: cache_rpath (dl-load.c:696)
==60268==    by 0x400ABF5: cache_rpath (dl-load.c:677)
==60268==    by 0x400ABF5: _dl_map_object (dl-load.c:2165)
==60268==    by 0x4003494: openaux (dl-deps.c:64)
==60268==    by 0x4B16C27: _dl_catch_exception (dl-error-skeleton.c:208)
==60268==    by 0x4003C7B: _dl_map_object_deps (dl-deps.c:248)
==60268==    by 0x400EA0E: dl_open_worker_begin (dl-open.c:592)
==60268==    by 0x4B16C27: _dl_catch_exception (dl-error-skeleton.c:208)
==60268==    by 0x400DF99: dl_open_worker (dl-open.c:782)
==60268==  Address 0x789d969 is 9 bytes inside a block of size 15 alloc'd
==60268==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==60268==    by 0x40271FF: malloc (rtld-malloc.h:56)
==60268==    by 0x40271FF: strdup (strdup.c:42)
==60268==    by 0x4008594: decompose_rpath (dl-load.c:629)
==60268==    by 0x400ABF5: cache_rpath (dl-load.c:696)
==60268==    by 0x400ABF5: cache_rpath (dl-load.c:677)
==60268==    by 0x400ABF5: _dl_map_object (dl-load.c:2165)
==60268==    by 0x4003494: openaux (dl-deps.c:64)
==60268==    by 0x4B16C27: _dl_catch_exception (dl-error-skeleton.c:208)
==60268==    by 0x4003C7B: _dl_map_object_deps (dl-deps.c:248)
==60268==    by 0x400EA0E: dl_open_worker_begin (dl-open.c:592)
==60268==    by 0x4B16C27: _dl_catch_exception (dl-error-skeleton.c:208)
==60268==    by 0x400DF99: dl_open_worker (dl-open.c:782)
==60268==    by 0x4B16C27: _dl_catch_exception (dl-error-skeleton.c:208)
==60268==    by 0x400E34D: _dl_open (dl-open.c:883)
```
The thing to understand in that error is that there is a buffer of size `15` that has been allocated with `malloc()`. Then, later, the function `strncmp` reads `16` bytes in that buffer, that is, **`1 byte beyond`** the allocated buffer. This should not happen for obvious security reasons. If you read the `backtrace` below , you see that the buffer given to `dl_open_worker` (`dl_` stands for `dynamic loader`, which is, let's says, the equivalent of the `dll` loader in windows) seems invalid, at least it's last `byte`
i guess that:
  * it `may` be because the parameter given to `dlopen()`  leaks a `'\0'` in its end. 

so in order to ensure that, i am running gdb and debugging `python exercise23.py` directly, no choice.... So, here are the gdb backtrace when causing the invalid read from above:

```
(venv) ciotatsoft@ciotatsoft-IdeaPad:~/dev/ciotatpay$ gdb python3
GNU gdb (Ubuntu 12.1-0ubuntu1~22.04) 12.1
Copyright (C) 2022 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from python3...
(No debugging symbols found in python3)
(gdb) target remote | /usr/bin/vgdb --pid=63294
Remote debugging using | /usr/bin/vgdb --pid=63294
relaying data between gdb and process 63294
warning: remote target does not support file transfer, attempting to access files from local filesystem.
Reading symbols from /lib64/ld-linux-x86-64.so.2...
Reading symbols from /usr/lib/debug/.build-id/61/ef896a699bb1c2e4e231642b2e1688b2f1a61e.debug...
0x00000000040202b0 in _start () from /lib64/ld-linux-x86-64.so.2
(gdb) r
The "remote" target does not support "run".  Try "help target" or "continue".
(gdb) continue
Continuing.

Program received signal SIGTRAP, Trace/breakpoint trap.
strncmp () at ../sysdeps/x86_64/strcmp.S:172
172	../sysdeps/x86_64/strcmp.S: No such file or directory.
(gdb) bt full
#0  strncmp () at ../sysdeps/x86_64/strcmp.S:172
No locals.
#1  0x000000000400668e in is_dst (input=input@entry=0x78a0791 "ORIGIN/../lib", ref=ref@entry=0x402dd44 "ORIGIN")
    at ./elf/dl-load.c:216
        is_curly = false
        rlen = <optimized out>
#2  0x000000000400810f in _dl_dst_count (input=0x78a0791 "ORIGIN/../lib") at ./elf/dl-load.c:253
        len = <optimized out>
        cnt = 0
        cnt = <optimized out>
        len = <optimized out>
#3  expand_dynamic_string_token (l=l@entry=0x789d900, input=input@entry=0x78a0790 "$ORIGIN/../lib") at ./elf/dl-load.c:395
        cnt = <optimized out>
        total = <optimized out>
        result = <optimized out>
        __PRETTY_FUNCTION__ = "expand_dynamic_string_token"
#4  0x00000000040082b8 in fillin_rpath (rpath=<optimized out>, rpath@entry=0x78a0790 "$ORIGIN/../lib", 
    result=result@entry=0x78a07e0, sep=sep@entry=0x402ebaf ":", what=what@entry=0x402ddb0 "RUNPATH", 
    where=where@entry=0x789d890 "/lib/x86_64-linux-gnu/libLLVM-13.so.1", l=l@entry=0x789d900) at ./elf/dl-load.c:483
        dirp = <optimized out>
        to_free = 0x0
        len = 0
        cp = 0x78a0790 "$ORIGIN/../lib"
        nelems = 0
#5  0x0000000004008603 in decompose_rpath (sps=sps@entry=0x789dcc0, rpath=<optimized out>, l=l@entry=0x789d900, 
    what=what@entry=0x402ddb0 "RUNPATH") at ./elf/dl-load.c:654
        where = 0x789d890 "/lib/x86_64-linux-gnu/libLLVM-13.so.1"
        cp = <optimized out>
        result = 0x78a07e0
        nelems = <optimized out>
        errstring = 0x0
        copy = 0x78a0790 "$ORIGIN/../lib"
#6  0x000000000400abf6 in cache_rpath (what=0x402ddb0 "RUNPATH", tag=29, sp=0x789dcc0, l=0x789d900) at ./elf/dl-load.c:696
No locals.
--Type <RET> for more, q to quit, c to continue without paging--c
#7  cache_rpath (what=0x402ddb0 "RUNPATH", tag=29, sp=0x789dcc0, l=0x789d900) at ./elf/dl-load.c:677
No locals.
#8  _dl_map_object (loader=<optimized out>, name=0x9b71f15 "libedit.so.2", type=2, trace_mode=0, mode=-2147483648, nsid=<optimized out>) at ./elf/dl-load.c:2165
        namelen = 13
        fd = <optimized out>
        origname = 0x0
        realname = 0x0
        name_copy = <optimized out>
        l = <optimized out>
        fb = {len = 0, buf = "\000\000\000\000\000\000\000\000\374=?\024\000\000\000\000\000\000\000\200\002", '\000' <repeats 19 times>, "\017\000\000\000\000\000\000\000\000\000\000\200\002", '\000' <repeats 19 times>, "\002\000\000\000\000\000\000\000\000\000\000\200\002\000\000\000\000\251\377\376\037", '\000' <repeats 11 times>, "\002\000\000\000\000\000\000\000\000\000\000\200\002\000\000\000\260\001\212\a", '\000' <repeats 20 times>, "\340\262\003\004\000\000\000\000\034Ӊ\a", '\000' <repeats 12 times>, "\017", '\000' <repeats 15 times>, "\034Ӊ\a\000\000\000\000\260\001\212\a\000\000\000\000\300\374"...}
        __PRETTY_FUNCTION__ = "_dl_map_object"
        found_other_class = false
        stack_end = 0x1c1e51bc
#9  0x0000000004003495 in openaux (a=a@entry=0x1ffeffb000) at ./elf/dl-deps.c:64
        args = 0x1ffeffb000
#10 0x0000000004b16c28 in __GI__dl_catch_exception (exception=<optimized out>, operate=<optimized out>, args=<optimized out>) at ./elf/dl-error-skeleton.c:208
        errcode = 31
        c = {exception = 0x1ffeffafe0, errcode = 0x1ffeffabfc, env = {{__jmpbuf = {0, -8134794032097419906, -8, 162995989, 1, 126474496, -8134794031145312898, -8132212917020418690}, __mask_was_saved = 0, __saved_mask = {__val = {126474496, 10311950042568433022, 10314531156689132926, 0, 126472960, 10311950042404855166, 10314531156689132926, 0, 126472960, 10311950042409049470, 10314531156689132926, 0, 67141257, 137422155840, 137422156912, 258603392}}}}}
        old = 0x1ffeffb510
#11 0x0000000004003c7c in _dl_map_object_deps (map=map@entry=0x789d300, preloads=preloads@entry=0x0, npreloads=npreloads@entry=0, trace_mode=trace_mode@entry=0, open_mode=open_mode@entry=-2147483648) at ./elf/dl-deps.c:248
        dep = <optimized out>
        err = <optimized out>
        strtab = <optimized out>
        args = {map = 0x789d900, trace_mode = 0, open_mode = -2147483648, strtab = 0x987d430 "", name = 0x9b71f15 "libedit.so.2", aux = 0x62c5870}
        orig = <optimized out>
        d = 0xf69f980
        l = <optimized out>
        needed = <optimized out>
        nneeded = 1
        known = <optimized out>
        runp = <optimized out>
        tail = <optimized out>
        nlist = <optimized out>
        i = <optimized out>
        name = <optimized out>
        errno_saved = <optimized out>
        errno_reason = 0
        exception = {objname = 0x0, errstring = 0x0, message_buffer = 0x0}
        needed_space = {data = 0x1ffeffb040, length = 1024, __space = {__align = {__max_align_ll = 103569520, __max_align_ld = <invalid float value>}, __c = "pX,\006\000\000\000\000@\240\003\004", '\000' <repeats 12 times>, "\001\246\000\004\000\000\000\000\002\000\000\000\000\000\000\000\002\001\000\220\000\000\000\000\340\260\377\376\037", '\000' <repeats 23 times>, "\002\000\000\000\360\260\377\376\037\000\000\000\000\000\000\000\000\000\000\020", '\000' <repeats 24 times>, "Ͻ\255\a\000\000\000\000p\266\377\376\037\000\000\000\000\203\273\004\000\000\000\000\200\266\377\376\037\000\000\000\220҉\a\000\000\000\000\300\374\377\376\037\000\000\000\a\000\000\000\000\000\000\000@\003\000\000\000\000\000\000\177ELF\002\001\001\000\000\000\000\000\000\000\000\000\003\000"...}}
        __PRETTY_FUNCTION__ = "_dl_map_object_deps"
        old_l_initfini = <optimized out>
        l_initfini = <optimized out>
        map_index = <optimized out>
        l_reldeps = <optimized out>
#12 0x000000000400ea0f in dl_open_worker_begin (a=a@entry=0x1ffeffb7a0) at ./elf/dl-open.c:592
        args = 0x1ffeffb7a0
        file = 0x1ffeffba70 "/usr/lib/x86_64-linux-gnu/dri/radeonsi_dri.so"
        mode = -2147483390
        call_map = <optimized out>
        dst = <optimized out>
        new = 0x789d300
        __PRETTY_FUNCTION__ = "dl_open_worker_begin"
        r = <optimized out>
        reloc_mode = <optimized out>
        first = <optimized out>
        last = <optimized out>
        j = <optimized out>
        l = <optimized out>
        relocation_in_progress = <optimized out>
        any_tls = <optimized out>
#13 0x0000000004b16c28 in __GI__dl_catch_exception (exception=<optimized out>, operate=<optimized out>, args=<optimized out>) at ./elf/dl-error-skeleton.c:208
        errcode = 2
        c = {exception = 0x1ffeffb600, errcode = 0x1ffeffb50c, env = {{__jmpbuf = {137422157728, -8134794032091128450, -8, 137422157312, 2, 2147483906, -8134794032112099970, -8132212917020418690}, __mask_was_saved = 0, __saved_mask = {__val = {67186545, 1, 0, 77299072, 77501664, 126437568, 137422158176, 126467616, 0, 137422162608, 67198190, 126467616, 128821051, 16, 0, 126467616}}}}}
        old = 0x1ffeffb680
#14 0x000000000400df9a in dl_open_worker (a=a@entry=0x1ffeffb7a0) at ./elf/dl-open.c:782
        ex = {objname = 0x789d1af "/usr/lib/x86_64-linux-gnu/dri/tls/radeonsi_dri.so", errstring = 0x789d190 "cannot open shared object file", message_buffer = 0x789d190 "cannot open shared object file"}
        err = <optimized out>
        args = 0x1ffeffb7a0
        mode = <optimized out>
        new = <optimized out>
        init_args = <optimized out>
#15 0x0000000004b16c28 in __GI__dl_catch_exception (exception=<optimized out>, operate=<optimized out>, args=<optimized out>) at ./elf/dl-error-skeleton.c:208
        errcode = 2
        c = {exception = 0x1ffeffb780, errcode = 0x1ffeffb67c, env = {{__jmpbuf = {-2, -8134794032091128450, -8, 67349064, 2, 2147483906, -8134794032034505346, -8132212917020418690}, __mask_was_saved = 0, __saved_mask = {__val = {4096, 137422157584, 128820852, 137422157968, 77767962, 13, 137422157824, 4222451713, 137422158208, 137422158208, 137422158208, 137422158208, 137422158243, 137422162304, 137422158208, 137422162304}}}}}
        old = 0x1ffeffb880
#16 0x000000000400e34e in _dl_open (file=<optimized out>, mode=-2147483390, caller_dlopen=0x7acea1a <glPrimitiveBoundingBox+3610>, nsid=-2, argc=2, argv=<optimized out>, env=0x1ffefffce0) at ./elf/dl-open.c:883
        args = {file = 0x1ffeffba70 "/usr/lib/x86_64-linux-gnu/dri/radeonsi_dri.so", mode = -2147483390, caller_dlopen = 0x7acea1a <glPrimitiveBoundingBox+3610>, map = 0x789d300, nsid = 0, original_global_scope_pending_adds = 0, libc_already_loaded = true, worker_continue = false, argc = 2, argv = 0x1ffefffcc8, env = 0x1ffefffce0}
        exception = {objname = 0x1ffeffba70 "/usr/lib/x86_64-linux-gnu/dri/radeonsi_dri.so", errstring = 0x2 <error: Cannot access memory at address 0x2>, message_buffer = 0x1ffeffba70 "/usr/lib/x86_64-linux-gnu/dri/radeonsi_dri.so"}
        errcode = <optimized out>
        __PRETTY_FUNCTION__ = "_dl_open"
#17 0x0000000004a326bc in dlopen_doit (a=a@entry=0x1ffeffba10) at ./dlfcn/dlopen.c:56
        args = 0x1ffeffba10
#18 0x0000000004b16c28 in __GI__dl_catch_exception (exception=exception@entry=0x1ffeffb970, operate=<optimized out>, args=<optimized out>) at ./elf/dl-error-skeleton.c:208
        errcode = 0
        c = {exception = 0x1ffeffb970, errcode = 0x1ffeffb87c, env = {{__jmpbuf = {137422158279, -8134794031749292674, -8, 128821336, 128821365, 128821224, -8134794031698961026, -8132212917020418690}, __mask_was_saved = 0, __saved_mask = {__val = {1671352992, 332028511, 1671352992, 332028511, 1671352992, 332028511, 16772136857631278336, 0, 128821394, 29, 137422158448, 128821336, 128821365, 128821224, 78474469, 206158430256}}}}}
        old = 0x0
#19 0x0000000004b16cf3 in __GI__dl_catch_error (objname=0x1ffeffb9c8, errstring=0x1ffeffb9d0, mallocedp=0x1ffeffb9c7, operate=<optimized out>, args=<optimized out>) at ./elf/dl-error-skeleton.c:227
        exception = {objname = 0x1102 <error: Cannot access memory at address 0x1102>, errstring = 0x58005540 <error: Cannot access memory at address 0x58005540>, message_buffer = 0x789d190 "cannot open shared object file"}
        errorcode = <optimized out>
#20 0x0000000004a321ae in _dlerror_run (operate=operate@entry=0x4a32660 <dlopen_doit>, args=args@entry=0x1ffeffba10) at ./dlfcn/dlerror.c:138
        result = <optimized out>
        objname = 0x789d1af "/usr/lib/x86_64-linux-gnu/dri/tls/radeonsi_dri.so"
        errstring = 0x789d190 "cannot open shared object file"
        malloced = true
        errcode = <optimized out>
#21 0x0000000004a32748 in dlopen_implementation (dl_caller=<optimized out>, mode=<optimized out>, file=<optimized out>) at ./dlfcn/dlopen.c:71
        args = {file = 0x1ffeffba70 "/usr/lib/x86_64-linux-gnu/dri/radeonsi_dri.so", mode = 258, new = 0x3e8, caller = 0x7acea1a <glPrimitiveBoundingBox+3610>}
#22 ___dlopen (file=<optimized out>, mode=<optimized out>) at ./dlfcn/dlopen.c:81
No locals.
#23 0x0000000007acea1a in glPrimitiveBoundingBox () from /lib/x86_64-linux-gnu/libGLX_mesa.so.0
No symbol table info available.
#24 0x0000000007aceb0d in glPrimitiveBoundingBox () from /lib/x86_64-linux-gnu/libGLX_mesa.so.0
No symbol table info available.
#25 0x0000000007aad305 in ?? () from /lib/x86_64-linux-gnu/libGLX_mesa.so.0
No symbol table info available.
#26 0x0000000007ac3e9c in ?? () from /lib/x86_64-linux-gnu/libGLX_mesa.so.0
No symbol table info available.
#27 0x0000000007ab53b9 in ?? () from /lib/x86_64-linux-gnu/libGLX_mesa.so.0
No symbol table info available.
#28 0x0000000007ab0516 in ?? () from /lib/x86_64-linux-gnu/libGLX_mesa.so.0
No symbol table info available.
#29 0x0000000007ab0f78 in ?? () from /lib/x86_64-linux-gnu/libGLX_mesa.so.0
No symbol table info available.
#30 0x0000000006db779b in glXChooseFBConfig () from /lib/x86_64-linux-gnu/libGLX.so.0
No symbol table info available.
#31 0x00000000065f2e2e in ?? () from /lib/x86_64-linux-gnu/libffi.so.8
No symbol table info available.
#32 0x00000000065ef493 in ?? () from /lib/x86_64-linux-gnu/libffi.so.8
No symbol table info available.
#33 0x00000000065c0451 in ?? () from /usr/lib/python3.10/lib-dynload/_ctypes.cpython-310-x86_64-linux-gnu.so
No symbol table info available.
#34 0x00000000065c9ce2 in ?? () from /usr/lib/python3.10/lib-dynload/_ctypes.cpython-310-x86_64-linux-gnu.so
No symbol table info available.
#35 0x000000000025a7db in _PyObject_MakeTpCall ()
No symbol table info available.
#36 0x000000000025348e in _PyEval_EvalFrameDefault ()
No symbol table info available.
#37 0x00000000002643ac in _PyFunction_Vectorcall ()
No symbol table info available.
#38 0x000000000024d14a in _PyEval_EvalFrameDefault ()
No symbol table info available.
#39 0x00000000002643ac in _PyFunction_Vectorcall ()
No symbol table info available.
#40 0x000000000024d14a in _PyEval_EvalFrameDefault ()
No symbol table info available.
#41 0x00000000002643ac in _PyFunction_Vectorcall ()
No symbol table info available.
#42 0x000000000024d14a in _PyEval_EvalFrameDefault ()
No symbol table info available.
#43 0x0000000000272391 in ?? ()
No symbol table info available.
#44 0x0000000000273032 in PyObject_Call ()
No symbol table info available.
#45 0x000000000024f3b0 in _PyEval_EvalFrameDefault ()
No symbol table info available.
#46 0x0000000000272391 in ?? ()
No symbol table info available.
#47 0x000000000024e2fc in _PyEval_EvalFrameDefault ()
No symbol table info available.
#48 0x0000000000259964 in _PyObject_FastCallDictTstate ()
No symbol table info available.
#49 0x000000000026e594 in ?? ()
No symbol table info available.
#50 0x000000000025a77c in _PyObject_MakeTpCall ()
No symbol table info available.
#51 0x0000000000252e39 in _PyEval_EvalFrameDefault ()
No symbol table info available.
#52 0x00000000002643ac in _PyFunction_Vectorcall ()
No symbol table info available.
#53 0x0000000000252a72 in _PyEval_EvalFrameDefault ()
No symbol table info available.
#54 0x0000000000249766 in ?? ()
No symbol table info available.
#55 0x0000000000341456 in PyEval_EvalCode ()
No symbol table info available.
#56 0x0000000000346fed in ?? ()
No symbol table info available.
#57 0x0000000000264609 in ?? ()
No symbol table info available.
#58 0x000000000024f3b0 in _PyEval_EvalFrameDefault ()
No symbol table info available.
#59 0x00000000002643ac in _PyFunction_Vectorcall ()
No symbol table info available.
#60 0x0000000000252a72 in _PyEval_EvalFrameDefault ()
No symbol table info available.
#61 0x00000000002643ac in _PyFunction_Vectorcall ()
No symbol table info available.
#62 0x000000000024d14a in _PyEval_EvalFrameDefault ()
No symbol table info available.
#63 0x00000000002643ac in _PyFunction_Vectorcall ()
No symbol table info available.
#64 0x000000000024d005 in _PyEval_EvalFrameDefault ()
No symbol table info available.
#65 0x00000000002643ac in _PyFunction_Vectorcall ()
No symbol table info available.
#66 0x000000000024d005 in _PyEval_EvalFrameDefault ()
No symbol table info available.
#67 0x00000000002643ac in _PyFunction_Vectorcall ()
No symbol table info available.
#68 0x00000000002637f5 in ?? ()
No symbol table info available.
#69 0x0000000000279c0f in _PyObject_CallMethodIdObjArgs ()
No symbol table info available.
#70 0x0000000000278032 in PyImport_ImportModuleLevelObject ()
No symbol table info available.
#71 0x0000000000288528 in ?? ()
No symbol table info available.
#72 0x0000000000263b5e in ?? ()
No symbol table info available.
#73 0x000000000025a7db in _PyObject_MakeTpCall ()
No symbol table info available.
#74 0x0000000000252e39 in _PyEval_EvalFrameDefault ()
No symbol table info available.
#75 0x0000000000272391 in ?? ()
No symbol table info available.
#76 0x00000000002d2005 in ?? ()
No symbol table info available.
#77 0x00000000002d13b2 in ?? ()
No symbol table info available.
#78 0x0000000000260ad2 in PyObject_GetAttr ()
No symbol table info available.
#79 0x0000000000252713 in _PyEval_EvalFrameDefault ()
No symbol table info available.
#80 0x0000000000259964 in _PyObject_FastCallDictTstate ()
No symbol table info available.
#81 0x000000000026e594 in ?? ()
No symbol table info available.
#82 0x000000000025a77c in _PyObject_MakeTpCall ()
No symbol table info available.
#83 0x0000000000252e39 in _PyEval_EvalFrameDefault ()
No symbol table info available.
#84 0x0000000000249766 in ?? ()
No symbol table info available.
#85 0x0000000000341456 in PyEval_EvalCode ()
No symbol table info available.
#86 0x000000000036df08 in ?? ()
No symbol table info available.
#87 0x0000000000366d5b in ?? ()
No symbol table info available.
#88 0x000000000036dc55 in ?? ()
No symbol table info available.
#89 0x000000000036d138 in _PyRun_SimpleFileObject ()
No symbol table info available.
#90 0x000000000036ce33 in _PyRun_AnyFileObject ()
No symbol table info available.
#91 0x000000000035e0ae in Py_RunMain ()
No symbol table info available.
#92 0x000000000033434d in Py_BytesMain ()
No symbol table info available.
#93 0x00000000049cbd90 in __libc_start_call_main (main=main@entry=0x334310, argc=argc@entry=2, argv=argv@entry=0x1ffefffcc8) at ../sysdeps/nptl/libc_start_call_main.h:58
        self = <optimized out>
        result = <optimized out>
        unwind_buf = {cancel_jmp_buf = {{jmp_buf = {0, -8132205621077762690, 137422175432, 3359504, 6719608, 67346496, -8134794033827570306, -8132213211786797698}, mask_was_saved = 0}}, priv = {pad = {0x0, 0x0, 0x0, 0x0}, data = {prev = 0x0, cleanup = 0x0, canceltype = 0}}}
        not_first_call = <optimized out>
#94 0x00000000049cbe40 in __libc_start_main_impl (main=0x334310, argc=2, argv=0x1ffefffcc8, init=<optimized out>, fini=<optimized out>, rtld_fini=<optimized out>, stack_end=0x1ffefffcb8) at ../csu/libc-start.c:392
No locals.
#95 0x0000000000334245 in _start ()
No symbol table info available.
(gdb)
```

I'll keep you updated for this issue too.