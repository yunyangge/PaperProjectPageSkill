"""Local-only static preview with byte-range support for long-video seeking."""
import argparse
import functools
import http.server
import os
import re

class RangeHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        self.byte_count=None
        path=self.translate_path(self.path)
        header=self.headers.get('Range')
        if not header or not os.path.isfile(path):
            return super().send_head()
        size=os.path.getsize(path)
        match=re.fullmatch(r'bytes=(\d*)-(\d*)',header)
        if not match or not any(match.groups()) or size==0:
            self.send_error(416,'Unsupported byte range')
            return None
        first,last=match.groups()
        start=int(first) if first else max(0,size-int(last))
        end=min(size-1,int(last)) if first and last else size-1
        if start>end or start>=size:
            self.send_response(416)
            self.send_header('Content-Range',f'bytes */{size}')
            self.send_header('Content-Length','0')
            self.end_headers()
            return None
        stream=open(path,'rb')
        stream.seek(start)
        self.byte_count=end-start+1
        self.send_response(206)
        self.send_header('Content-Type',self.guess_type(path))
        self.send_header('Content-Length',str(self.byte_count))
        self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
        self.send_header('Accept-Ranges','bytes')
        self.end_headers()
        return stream

    def end_headers(self):
        if self.byte_count is None:
            self.send_header('Accept-Ranges','bytes')
        super().end_headers()

    def copyfile(self,source,outputfile):
        remaining=self.byte_count
        try:
            while remaining is None or remaining>0:
                chunk=source.read(65536 if remaining is None else min(65536,remaining))
                if not chunk:break
                outputfile.write(chunk)
                if remaining is not None:remaining-=len(chunk)
        except (BrokenPipeError,ConnectionResetError,ConnectionAbortedError):
            pass  # A browser may cancel an obsolete media request on prompt switch.

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--port',type=int,default=8767)
    parser.add_argument('--directory',default='outputs/benchmarks')
    args=parser.parse_args()
    server=http.server.ThreadingHTTPServer(('127.0.0.1',args.port),functools.partial(RangeHandler,directory=args.directory))
    print(f'Local media preview: http://127.0.0.1:{args.port}',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:server.server_close()
