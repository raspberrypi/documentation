## Overview
This page describes the procedure for accessing a mailbox from code running on the ARM side of the mailbox interface.

## General procedure
To read from a mailbox:

1. Read the status register until the empty flag is not set
2. Read data from the read register
3. If the lower four bits do not match the channel number desired then repeat from 1
4. The upper 28 bits are the returned data

To write to a mailbox

1. Read the status register until the full flag is not set
2. Write the data (shifted into the upper 28 bits) combined with the channel (in the lower four bits) to the write register

## Addresses as data
With the exception of the property tags mailbox channel, when passing memory addresses as the data part of a mailbox message, the addresses should be bus addresses as seen from the VC.
These vary depending on whether the L2 cache is enabled. If it is, physical memory is mapped to start at 0x40000000 by the VC MMU; if L2 caching is disabled, physical memory is mapped to start at 0xC0000000 by the VC MMU.
Returned addresses (both those returned in the data part of the mailbox response and any written into the buffer you passed) will also be as mapped by the VC MMU. In the exceptional case when you are using the property tags mailbox channel you should send and receive physical addresses (the same as you'd see from the ARM before enabling the MMU).

For example, if you have created a framebuffer description structure in memory (without having enabled the ARM MMU) at 0x00010000 and you have not changed config.txt to disable the L2 cache, to send it to channel 1 you would send 0x40010001 (0x40000000 | 0x00010000 | 0x1) to the mailbox. 
Your structure would be updated to include a framebuffer address starting from 0x40000000 (e.g. 0x4D385000) and you would write to it using the corresponding ARM physical address (e.g. 0x0D385000).

## Memory barriers & Invalidating/flushing data cache
Memory barriers or data cache invalidation/flushing may be required around mailbox accesses, details on this needs to be added to this page (or the page for the particular mailbox/channel that requires it) by someone who knows the details.

The following instructions are taken from http://infocenter.arm.com/help/topic/com.arm.doc.ddi0360f/I1014942.html. Any unneeded register can be used in the following example instead of r3.

The following instructions are taken from http://infocenter.arm.com/help/topic/com.arm.doc.ddi0360f/I1014942.html. Any unneeded register can be used in the following example instead of r3.
````
mov r3, #0				# The read register Should Be Zero before the call
mcr p15, 0, r3, C7, C6, 0		# Invalidate Entire Data Cache
mcr p15, 0, r3, c7, c10, 0		# Clean Entire Data Cache
mcr p15, 0, r3, c7, c14, 0		# Clean and Invalidate Entire Data Cache
mcr p15, 0, r3, c7, c10, 4		# Data Synchronization Barrier
mcr p15, 0, r3, c7, c10, 5		# Data Memory Barrier
````
The following procedure is used sometimes around physical device accesses.
````
MemoryBarrier:
	mcr p15, 0, r3, c7, c5, 0	# Invalidate instruction cache
	mcr p15, 0, r3, c7, c5, 6	# Invalidate BTB
	mcr p15, 0, r3, c7, c10, 4	# Drain write buffer
	mcr p15, 0, r3, c7, c5, 4	# Prefetch flush
	mov pc, lr					# Return
````

## Sample code
This code is untested and is written for clarity rather than brevity or efficiency, but is provided for convenience.

````c++
#define MAIL_BASE 0xB880	// Base address for the mailbox registers

// This bit is set in the status register if there is no space to write into the mailbox
#define MAIL_FULL 0x80000000
// This bit is set in the status register if there is nothing to read from the mailbox
#define MAIL_EMPTY 0x40000000

uint32 ReadMailbox(byte channel)
{
	// Loop until we receive something from the requested channel
	for (;;)
	{
		while ((ReadMemMappedReg<uint32>(MAIL_BASE, ReadStatusOffset) & MAIL_EMPTY) != 0)
		{
			// Wait for data
		}
		// Read the data
		uint32 data = ReadMemMappedReg<uint32>(MAIL_BASE, ReadOffset);
		byte readChannel = data & 0xF;
		data >>= 4;
		// Return it straight away if it's for the requested channel
		if (readChannel == channel)
			return data;
	}
}

void WriteMailbox(byte channel, uint32 data)
{
	while ((ReadMemMappedReg<uint32>(MAIL_BASE, WriteStatusOffset) & MAIL_FULL) != 0)
	{
		// Wait for space
	}
	// Write the value to the requested channel
	WriteMemMappedReg(MAIL_BASE, WriteOffset, (data << 4) | channel);
}

#define MAPPED_REGISTERS_BASE 0x20000000

template<class T>
static T ReadMemMappedReg(size_t BaseAddress, size_t Offset)
{
	return *reinterpret_cast<const T *>(MAPPED_REGISTERS_BASE + BaseAddress + Offset);
}

template<class T>
static void WriteMemMappedReg(size_t BaseAddress, size_t Offset, T Data)
{
	*reinterpret_cast<T *>(MAPPED_REGISTERS_BASE + BaseAddress + Offset) = Data;
}
````
