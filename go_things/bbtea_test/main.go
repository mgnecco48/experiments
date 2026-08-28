package main

import (
	"fmt"
	"os"

	tea "charm.land/bubbletea/v2"
)

// TODO: need to fix the cursor drawing logic

type model struct {
	tasks    []string
	cursor   int
	selected map[int]struct{}
}

func initialModel() model {
	return model{
		tasks:    []string{"Make bed", "Study", "Go to work"},
		selected: make(map[int]struct{}),
	}
}

func (m model) Init() tea.Cmd {
	return nil
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyPressMsg:
		switch msg.String() {
		case "ctrl+c", "q":
			return m, tea.Quit
		case "up", "k":
			if m.cursor > 0 {
				m.cursor--
			}
		case "down", "j":
			if m.cursor < len(m.tasks)-1 {
				m.cursor++
			}
		case "enter", "space":
			_, ok := m.selected[m.cursor]
			if ok {
				delete(m.selected, m.cursor)
			} else {
				m.selected[m.cursor] = struct{}{}
			}
		}
	}
	return m, nil
}

func (m model) View() tea.View {
	s := "Today's Tasks:\n\n"

	for i, choice := range m.tasks {
		cursor := " "
		if m.cursor == i {
			cursor = ">"
		}

		completed := " "
		if _, ok := m.selected[i]; ok {
			completed = "✔︎"
		}

		s += fmt.Sprintf("%s [%s] %s\n", cursor, completed, choice)
	}

	s += "\nPress q or ctrl+c to quit.\n"

	return tea.NewView(s)

}

func main() {
	p := tea.NewProgram(initialModel())
	if _, err := p.Run(); err != nil {
		fmt.Print("There was a problem 😭")
		os.Exit(1)
	}
}
