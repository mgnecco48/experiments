package main

import (
	"fmt"
	"os"

	"charm.land/bubbletea/v2"
	"github.com/charmbracelet/lipgloss"
)

type model struct {
	choices  []string
	selected map[int]struct{}
	cursor   int
	input    string
	adding   bool
}

func initialModel() model {
	return model{
		choices:  []string{},
		selected: make(map[int]struct{}),
	}
}

func (m model) Init() tea.Cmd {
	return nil
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyPressMsg:
		if m.adding {
			switch msg.String() {
			case "escape":
				m.adding = false
				m.input = ""
				return m, nil
			case "ctrl+enter", "ctrl+m":
				if m.input != "" {
					m.choices = append(m.choices, m.input)
					m.input = ""
					m.adding = false
				}
				return m, nil
			case "enter":
				return m, nil
			case "backspace":
				if len(m.input) > 0 {
					m.input = m.input[:len(m.input)-1]
				}
				return m, nil
			default:
				char := msg.String()
				if len(char) == 1 && char[0] >= 32 && char[0] < 127 {
					m.input += char
				}
				return m, nil
			}
		}

		switch msg.String() {
		case "ctrl+c", "q":
			return m, tea.Quit

		case "a":
			m.adding = true
			return m, nil

		case "enter", " ":
			if len(m.choices) > 0 {
				_, ok := m.selected[m.cursor]
				if ok {
					delete(m.selected, m.cursor)
				} else {
					m.selected[m.cursor] = struct{}{}
				}
				return m, nil
			}

		case "up", "k":
			if m.cursor > 0 {
				m.cursor--
			}

		case "down", "j":
			if m.cursor < len(m.choices)-1 {
				m.cursor++
			}

		case "d":
			if len(m.choices) > 0 {
				m.choices = append(m.choices[:m.cursor], m.choices[m.cursor+1:]...)
				delete(m.selected, m.cursor)
				if m.cursor >= len(m.choices) && m.cursor > 0 {
					m.cursor--
				}
			}
		}

	case tea.PasteMsg:
		if m.adding {
			m.input += msg.String()
			return m, nil
		}
	}

	return m, nil
}

func (m model) View() tea.View {
	doc := ""

	headerStyle := lipgloss.NewStyle().
		Foreground(lipgloss.Color("205")).
		Bold(true).
		Align(lipgloss.Center)

	itemStyle := lipgloss.NewStyle().
		Foreground(lipgloss.Color("252"))

	selectedStyle := lipgloss.NewStyle().
		Foreground(lipgloss.Color("229"))

	cursorStyle := lipgloss.NewStyle().
		Foreground(lipgloss.Color("205")).
		Bold(true)

	inputStyle := lipgloss.NewStyle().
		Foreground(lipgloss.Color("86"))

	boxStyle := lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.Color("240")).
		Padding(1, 2)

	doc += "\n"
	doc += headerStyle.Render("  Shopping List  ") + "\n\n"

	if len(m.choices) == 0 && !m.adding {
		doc += itemStyle.Render("  No items yet. Press 'a' to add something!") + "\n\n"
	}

	for i, choice := range m.choices {
		cursor := "  "
		if m.cursor == i {
			cursor = cursorStyle.Render(" >")
		}

		checked := "[ ]"
		if _, ok := m.selected[i]; ok {
			checked = selectedStyle.Render("[x]")
		}

		row := fmt.Sprintf("%s %s %s\n", cursor, checked, itemStyle.Render(choice))
		doc += row
	}

	doc += "\n"

	if m.adding {
		doc += fmt.Sprintf("  %s %s%s %s\n", cursorStyle.Render(">"),
			inputStyle.Render(m.input), lipgloss.NewStyle().Foreground(lipgloss.Color("240")).Render("_"), lipgloss.NewStyle().Foreground(lipgloss.Color("245")).Render("(ctrl+enter to add, esc to cancel)"))
	}

	doc += "\n"
	doc += boxStyle.Render(fmt.Sprintf("  %s %s %s %s",
		itemStyle.Render("[↑↓] navigate"),
		itemStyle.Render("[space] toggle"),
		itemStyle.Render("[a] add"),
		itemStyle.Render("[d] delete"),
	))
	doc += "\n"
	doc += itemStyle.Render("  Press 'q' to quit\n")

	return tea.NewView(doc)
}

func main() {
	p := tea.NewProgram(initialModel())
	if _, err := p.Run(); err != nil {
		fmt.Printf("Error: %v", err)
		os.Exit(1)
	}
}
