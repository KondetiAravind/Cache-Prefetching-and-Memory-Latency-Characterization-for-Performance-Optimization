/* cache.h - cache module interfaces */

/* SimpleScalar(TM) Tool Suite
 * Copyright (C) 1994-2003 by Todd M. Austin, Ph.D. and SimpleScalar, LLC.
 * All Rights Reserved. 
 */

#ifndef CACHE_H
#define CACHE_H

#include <stdio.h>

#include "host.h"
#include "misc.h"
#include "machine.h"
#include "memory.h"
#include "stats.h"

/* highly associative caches use hash tables */
#define CACHE_HIGHLY_ASSOC(cp)	((cp)->assoc > 4)

/* cache replacement policy */
enum cache_policy {
  LRU,
  Random,
  FIFO
};

/* block status */
#define CACHE_BLK_VALID		0x00000001
#define CACHE_BLK_DIRTY		0x00000002

/* cache block structure */
struct cache_blk_t
{
  struct cache_blk_t *way_next;
  struct cache_blk_t *way_prev;
  struct cache_blk_t *hash_next;
  md_addr_t tag;
  unsigned int status;
  tick_t ready;
  byte_t *user_data;
  byte_t data[1];
};

/* cache set structure */
struct cache_set_t
{
  struct cache_blk_t **hash;
  struct cache_blk_t *way_head;
  struct cache_blk_t *way_tail;
  struct cache_blk_t *blks;
};

/* cache structure */
struct cache_t
{
  /* parameters */
  char *name;
  int nsets;
  int bsize;
  int balloc;
  int usize;
  int assoc;
  enum cache_policy policy;
  unsigned int hit_latency;

  /* miss/replacement handler */
  unsigned int
  (*blk_access_fn)(enum mem_cmd cmd,
                   md_addr_t baddr,
                   int bsize,
                   struct cache_blk_t *blk,
                   tick_t now);

  /* derived parameters */
  int hsize;
  md_addr_t blk_mask;
  int set_shift;
  md_addr_t set_mask;
  int tag_shift;
  md_addr_t tag_mask;
  md_addr_t tagset_mask;

  /* bus resource */
  tick_t bus_free;

  /* stats */
  counter_t hits;
  counter_t misses;
  counter_t replacements;
  counter_t writebacks;
  counter_t invalidations;

  /* NEW FIELDS FOR PREFETCH */
  unsigned long long prefetch_count;  /* total number of prefetches issued */
  int in_prefetch;                    /* flag to prevent recursive calls */

  /* fast hit tracking */
  md_addr_t last_tagset;
  struct cache_blk_t *last_blk;

  /* data blocks */
  byte_t *data;

  /* sets */
  struct cache_set_t sets[1];
};

/* function declarations */
struct cache_t *
cache_create(char *name,
	     int nsets,
	     int bsize,
	     int balloc,
	     int usize,
	     int assoc,
	     enum cache_policy policy,
	     unsigned int (*blk_access_fn)(enum mem_cmd cmd,
					   md_addr_t baddr, int bsize,
					   struct cache_blk_t *blk,
					   tick_t now),
	     unsigned int hit_latency);

enum cache_policy cache_char2policy(char c);
void cache_config(struct cache_t *cp, FILE *stream);
void cache_reg_stats(struct cache_t *cp, struct stat_sdb_t *sdb);
void cache_stats(struct cache_t *cp, FILE *stream);

unsigned int
cache_access(struct cache_t *cp,
	     enum mem_cmd cmd,
	     md_addr_t addr,
	     void *vp,
	     int nbytes,
	     tick_t now,
	     byte_t **udata,
	     md_addr_t *repl_addr);

#define cache_double(cp, cmd, addr, p, now, udata)	\
  cache_access(cp, cmd, addr, p, sizeof(double), now, udata)
#define cache_float(cp, cmd, addr, p, now, udata)	\
  cache_access(cp, cmd, addr, p, sizeof(float), now, udata)
#define cache_dword(cp, cmd, addr, p, now, udata)	\
  cache_access(cp, cmd, addr, p, sizeof(long long), now, udata)
#define cache_word(cp, cmd, addr, p, now, udata)	\
  cache_access(cp, cmd, addr, p, sizeof(int), now, udata)
#define cache_half(cp, cmd, addr, p, now, udata)	\
  cache_access(cp, cmd, addr, p, sizeof(short), now, udata)
#define cache_byte(cp, cmd, addr, p, now, udata)	\
  cache_access(cp, cmd, addr, p, sizeof(char), now, udata)

int cache_probe(struct cache_t *cp, md_addr_t addr);
unsigned int cache_flush(struct cache_t *cp, tick_t now);
unsigned int cache_flush_addr(struct cache_t *cp, md_addr_t addr, tick_t now);

#endif /* CACHE_H */
