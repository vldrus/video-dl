/*
Copyright (c) 2026 Vlad

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

#include <iostream>
#include <sstream>
#include <string>

#include <cstdlib>
#include <cstdio>

#ifdef _WIN32
#include <direct.h>
#else
#include <unistd.h>
#endif

using std::cin;
using std::cout;
using std::string;
using std::getline;
using std::stringstream;

using std::FILE;
using std::exit;
using std::fgets;
using std::getenv;
using std::system;

const string exe_file = "yt-dlp"; // https://github.com/yt-dlp/yt-dlp

template <typename... T>
void print(const T... args)
{
    stringstream fmt;

    ((fmt << args << " "), ...);

    string result = fmt.str();

    if (result.length() > 0) {
        result.resize(result.length() - 1);
    }

    cout << result + "\n";
}

string input(const string message)
{
    cout << message;

    string result;
    getline(cin, result);

    return result;
}

string wrap_with_quotes(const string str)
{
    return "\"" + str + "\"";
}

[[noreturn]]
void exit_with_pause(int exit_code, bool need_pause)
{
    if (need_pause) {
        print();
        input("Press <Enter> to close...");
    }

    exit(exit_code);
}

[[noreturn]]
int main(int argc, char* argv[])
{
    bool need_pause = argc < 2;

#ifdef _WIN32
    _chdir((getenv("USERPROFILE") + string("\\Downloads")).c_str());
#else
    string xdg_download_dir_cmd = "echo -n $(xdg-user-dir DOWNLOAD 2>&1) 2>&1";
    FILE* xdg_download_dir_stream = popen(xdg_download_dir_cmd.c_str(), "r");

    if (xdg_download_dir_stream != nullptr) {
        char buf[128];

        fgets(buf, 128, xdg_download_dir_stream);

        if (chdir(buf) != 0) {
            chdir((getenv("HOME") + string("/Downloads")).c_str());
        }

        pclose(xdg_download_dir_stream);
    } else {
        chdir((getenv("HOME") + string("/Downloads")).c_str());
    }
#endif

    string cmd_line = wrap_with_quotes(exe_file) +
                      " --update";

    if (system(cmd_line.c_str()) != 0) {
        exit_with_pause(1, need_pause);
    }

    print();

    string video_link;

    if (argc > 1) {
        video_link = argv[1];
        print("Video link:", video_link);
    } else {
        video_link = input("Enter video link: ");
    }

    print();

    cmd_line = wrap_with_quotes(exe_file) +
               " --no-playlist --list-formats " +
               wrap_with_quotes(video_link);

    if (system(cmd_line.c_str()) != 0) {
        exit_with_pause(1, need_pause);
    }

    print();

    string video_format = input("Enter download format: ");

    print();

    string video_output = "%(id)s.%(ext)s";
    string video_merge = "mkv";

    cmd_line = wrap_with_quotes(exe_file) +
               " --no-playlist --format " +
               wrap_with_quotes(video_format) +
               " --output " +
               wrap_with_quotes(video_output) +
               " --merge-output-format " +
               wrap_with_quotes(video_merge) +
               " " +
               wrap_with_quotes(video_link);

    if (system(cmd_line.c_str()) != 0) {
        exit_with_pause(1, need_pause);
    }

    exit_with_pause(0, need_pause);
}
