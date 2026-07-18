# Sprint 4 Retrospective

## UX Decisions

- Responsive dashboard layout
- Sidebar navigation
- Interactive Plotly charts
- CSV download support
- Preset screeners

---

## Data Edge Cases

- Companies with less than 10 years of data
- Missing financial metrics
- Empty screener results
- Missing annual reports

---

## Performance Findings

- Cached database queries
- Streamlit cache enabled
- Company Profile loads under 3 seconds
- Responsive charts

---

## Lessons Learned

- Database caching significantly improves performance.
- Defensive handling of missing values improves stability.
- Responsive layouts improve usability across different screen sizes.