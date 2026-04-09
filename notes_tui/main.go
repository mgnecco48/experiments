package main

import (
	"fmt"
	"os"
	"path/filepath"

	"charm.land/bubbles/v2/viewport"
	tea "charm.land/bubbletea/v2"
	"charm.land/glamour/v2"
	"charm.land/lipgloss/v2"
)

type Note struct {
	Title string
	Path  string
}

type model struct {
	notes   []Note
	cursor  int
	content string
	viewing bool

	width  int
	height int

	viewport viewport.Model
	renderer *glamour.TermRenderer
}

// COLOR STYLES FROM LIPGLOSS
var (
	cursorStyle = lipgloss.NewStyle().
		Foreground(lipgloss.Color("212"))
)

func loadNotes(path string) []Note {
	files, err := os.ReadDir(path)
	if err != nil {
		return nil
	}
	var notes []Note

	for _, file := range files {
		name := file.Name()
		fullPath := filepath.Join(path, name)

		note := Note{
			Title: name,
			Path:  fullPath,
		}
		notes = append(notes, note)
	}

	return notes
}

func initialModel() model {
	return model{
		notes:    loadNotes("/Users/martin/Documents/notes/"),
		viewport: viewport.Model{},
	}
}

func (m model) Init() tea.Cmd {
	return nil
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {

	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height
		titleHeight := 3
		hintHeight := 3
		contentHeight := m.height - titleHeight - hintHeight // adjust if needed

		m.viewport.SetWidth(m.width)
		m.viewport.SetHeight(contentHeight)

	case tea.KeyPressMsg:

		switch msg.String() {

		case "ctrl+c", "q":
			if m.viewing {
				m.viewing = false
				return m, nil
			}
			return m, tea.Quit

		case "up", "k":
			if !m.viewing {

				if m.cursor > 0 {
					m.cursor--
				}
			}

		case "down", "j":
			if !m.viewing {
				if m.cursor < len(m.notes)-1 {
					m.cursor++
				}
			}

		case "enter":
			note := m.notes[m.cursor]
			content, err := os.ReadFile(note.Path)
			if err == nil {
				m.content = string(content)
				m.viewing = true
				text, err := glamour.Render(m.content, "dark")
				if err != nil {
					text = "NO CONTENT"
				}
				m.viewport.SetContent(text)
			}
		}
	}

	// let viewport handle scrolling when viewing
	if m.viewing {
		var cmd tea.Cmd
		m.viewport, cmd = m.viewport.Update(msg)
		return m, cmd
	}

	return m, nil
}

func (m model) View() tea.View {
	titleStyle := lipgloss.NewStyle().
		Width(m.width).
		Align(lipgloss.Center).
		Foreground(lipgloss.BrightWhite).
		Bold(true).
		BorderStyle(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.BrightWhite)

	hintStyle := lipgloss.NewStyle().
		Width(m.width).
		Align(lipgloss.Center).
		Foreground(lipgloss.White).Faint(true)

	if m.viewing {
		fileName := m.notes[m.cursor]

		title := titleStyle.Render(fileName.Title)
		hint := hintStyle.Render("Press q to go back")

		usedHeight := lipgloss.Height(title) + lipgloss.Height(hint)
		contentHeight := m.height - usedHeight

		contentStyle := lipgloss.NewStyle().
			Width(m.width).
			Height(contentHeight).
			Align(lipgloss.Center).
			Foreground(lipgloss.BrightWhite).
			BorderStyle(lipgloss.RoundedBorder()).
			BorderForeground(lipgloss.BrightWhite)

		content := contentStyle.Render(m.viewport.View())

		v := tea.NewView(title + "\n" + content + "\n" + hint)
		v.AltScreen = true

		return v
	}

	var notesList string

	for i, note := range m.notes {
		cursor := " "
		if m.cursor == i {
			cursor = ">"
		}

		line := fmt.Sprintf("%s %s", cursor, note.Title)

		if m.cursor == i {
			line = cursorStyle.Render(line)
		}

		notesList += line + "\n"
	}

	title := titleStyle.Render("NOTES")
	hint := hintStyle.Render("Press q to go back")

	usedHeight := lipgloss.Height(title) + lipgloss.Height(hint)
	contentHeight := m.height - usedHeight

	contentStyle := lipgloss.NewStyle().
		Width(m.width).
		Height(contentHeight).
		Align(lipgloss.Left).
		Foreground(lipgloss.BrightWhite).
		BorderStyle(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.BrightWhite)

	content := contentStyle.Render(notesList)

	v := tea.NewView(title + "\n" + content + "\n" + hint)
	v.AltScreen = true

	return v
}

func main() {
	p := tea.NewProgram(initialModel())
	if _, err := p.Run(); err != nil {
		fmt.Printf("Alas, there's been an error: %v", err)
		os.Exit(1)
	}
}
