package main

import (
    "os/exec"
    "strings"
    "bytes"
    "fmt"
)

func dfs(current string, last rune) {
    hoge := "wasd"
    for _, next := range hoge {
        if (next == 'w' && last == 's' || next == 's' && last == 'w' || next == 'a' && last == 'd' || next == 'd' && last == 'a') {
            continue
        }
        var out bytes.Buffer
        cmd := exec.Command("trydbg.exe")
        cmd.Stdin = strings.NewReader(current)
        cmd.Stdout = &out
        _ = cmd.Run()

        if strings.Contains(out.String(), "wrong way") {
            continue
        }
        fmt.Println(current + string(next))
        dfs(current + string(next), next)
    }
}

func main() {
    dfs("", 'i');
}
