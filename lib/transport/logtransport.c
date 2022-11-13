/*
 * Copyright (c) 2002-2013 Balabit
 * Copyright (c) 1998-2013 Balázs Scheidler
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 * As an additional exemption you are allowed to compile & link against the
 * OpenSSL libraries as published by the OpenSSL project. See the file
 * COPYING for details.
 *
 */

#include "logtransport.h"
#include "messages.h"

#include <unistd.h>

/*
 * log_transport_read_chunk():
 *
 * Reads up to count bytes even if we need multiple read invocations.
 *   * it attempts to read as many bytes as requested (e.g. count)
 *
 *   * if we encounter an error during reading of the input, that error is
 *     returned, potentially discarding partial data.
 *
 *   * if we encounter EOF we return partial data (or EOF it we don't have
 *     partial data)
 *
 *   * if we encounter EAGAIN, we return partial data (e.g.  this is not a
 *     busy loop)
 *
 * Returns: the number of bytes read
 */
gssize
log_transport_read_chunk(LogTransport *self, gpointer buf, gsize count, LogTransportAuxData *aux)
{
  gsize bytes_so_far = 0;
  gssize rc = 1;

  while (bytes_so_far < count)
    {
      rc = log_transport_read(self,
                              (gchar *) buf + bytes_so_far, count - bytes_so_far,
                              bytes_so_far == 0 ? aux : NULL);

      if (rc < 0)
        {
          if (errno == EAGAIN && bytes_so_far == 0)
            {
              /* EAGAIN at first read(): return EAGAIN to the caller */
              return rc;
            }
          if (errno != EAGAIN)
            {
              /* error, return the error.  We might have some buffered data
               * already, which is discarded */
              return rc;
            }
          /* we can't read anymore, exit the loop and return the data read so far */
          break;
        }
      else if (rc > 0)
        {
          /* some data was read, let's continue and see if it was enough */
          bytes_so_far += rc;
        }
      else if (rc == 0)
        {
          /* EOF, we return the data we consumed so far */
          break;
        }
    }
  return bytes_so_far;
}

void
log_transport_free_method(LogTransport *s)
{
  if (s->fd != -1)
    {
      msg_trace("Closing log transport fd",
                evt_tag_int("fd", s->fd));
      close(s->fd);
    }
}

void
log_transport_init_instance(LogTransport *self, gint fd)
{
  self->fd = fd;
  self->cond = 0;
  self->free_fn = log_transport_free_method;
}

void
log_transport_free(LogTransport *self)
{
  self->free_fn(self);
  g_free(self);
}

gint
log_transport_release_fd(LogTransport *s)
{
  gint fd = s->fd;
  s->fd = -1;

  return fd;
}

