package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"net"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"syscall"
)

var waybarPid int
var socketPath = os.Getenv("NIRI_SOCKET")

const STATE_FILE = "/tmp/waybar-visible"

const (
	windowOpenedOrChanged        = "WindowOpenedOrChanged"
	workspaceActiveWindowChanged = "WorkspaceActiveWindowChanged"
	workspaceActivated           = "WorkspaceActivated"
	overviewOpenedOrClosed       = "OverviewOpenedOrClosed"
	windowFocusChanged           = "WindowFocusChanged"
)

func init() {
	out, err := exec.Command("pgrep", "waybar").Output()
	if err != nil {
		fmt.Fprintln(os.Stderr, "Waybar not found error: ", err)
		os.Exit(1)
	}
	file, err := os.Create(STATE_FILE)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Create file error: ", err)
	}
	file.Close()

	pids := strings.Split(string(out), "\n")
	pids = pids[:len(pids)-1]

	waybarPid, err = strconv.Atoi(pids[0])
	fmt.Println("Waybar PID:", waybarPid)
	if err != nil {
		fmt.Fprintln(os.Stderr, "PID parse error: ", err)
		os.Exit(0)
	}
}

func toggleWaybar() {
	if err := syscall.Kill(waybarPid, syscall.SIGUSR1); err != nil {
		fmt.Fprintln(os.Stderr, "Waybar toggle error: ", err)
	}
}

func showWaybar() {
	if _, err := os.Stat(STATE_FILE); os.IsNotExist(err) {
		toggleWaybar()
		file, err := os.Create(STATE_FILE)
		if err != nil {
			fmt.Fprintln(os.Stderr, "Create file error: ", err)
		}
		file.Close()
	}
}

func hideWaybar() {
	if _, err := os.Stat(STATE_FILE); err == nil {
		toggleWaybar()
		if err := os.Remove(STATE_FILE); err != nil {
			fmt.Fprintln(os.Stderr, "Delete file error: ", err)
		}
	}
}

func AutoToggle(conn net.Conn) {
	result := sendEvent(conn, "FocusedWindow")
	if result == nil {
		return
	}
	var raw map[string]any
	if err := json.Unmarshal(result, &raw); err != nil {
		fmt.Fprintln(os.Stderr, "Unmarshal error: ", err)
		return
	}
	fwOk := raw["Ok"].(map[string]any)
	if fwOk["FocusedWindow"] == nil {
		showWaybar()
		return
	}
	/* Comment out all the lines below except hideWaybar() to hide waybar on focused floating window */
	fw := fwOk["FocusedWindow"].(map[string]any)
	isFloating := fw["is_floating"].(bool)
	if isFloating {
		showWaybar()
	} else {
		hideWaybar()
	}
}

func sendEvent(conn net.Conn, eventType string) []byte {
	msg := fmt.Sprintf("\"%s\"\n", eventType)
	if _, err := conn.Write([]byte(msg)); err != nil {
		fmt.Fprintln(os.Stderr, "Write error: ", err)
		return nil
	}
	reader := bufio.NewReader(conn)
	response, err := reader.ReadBytes('\n')
	if err != nil {
		fmt.Fprintln(os.Stderr, "Read error: ", err)
		return nil
	}
	return response
}

func main() {
	streamConn, err := net.Dial("unix", socketPath)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Dial error: ", err)
		os.Exit(1)
	}
	defer streamConn.Close()

	eventConn, err := net.Dial("unix", socketPath)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Dial error", err)
		return
	}
	defer eventConn.Close()

	if _, err = streamConn.Write([]byte("\"EventStream\"\n")); err != nil {
		fmt.Fprintln(os.Stderr, "Write error: ", err)
		return
	}

	scanner := bufio.NewScanner(streamConn)

	var overviewMode = false
	for scanner.Scan() {
		line := scanner.Text()

		var event map[string]any
		if err = json.Unmarshal([]byte(line), &event); err != nil {
			fmt.Fprintln(os.Stderr, "Unmarshal error: ", err)
			continue
		}

		if event[overviewOpenedOrClosed] != nil {
			var raw map[string]any
			if err := json.Unmarshal([]byte(line), &raw); err != nil {
				fmt.Fprintln(os.Stderr, "Unmarshal error: ", err)
				continue
			}
			overviewMode = (raw["OverviewOpenedOrClosed"].(map[string]any))["is_open"].(bool)
			if overviewMode {
				showWaybar()
			} else {
				AutoToggle(eventConn)
			}
		} else if !overviewMode && (event[workspaceActiveWindowChanged] != nil || event[windowOpenedOrChanged] != nil || event[workspaceActivated] != nil || event[windowFocusChanged] != nil) {
			AutoToggle(eventConn)
		}

	}

}
