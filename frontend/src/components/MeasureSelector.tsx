import { Checkbox, FormControlLabel, List, ListItemButton, ListSubheader } from '@mui/material'
import { Measure } from '../types'

type Props = { measures: Measure[]; selected: string[]; onChange: (next: string[]) => void }
export default function MeasureSelector({ measures, selected, onChange }: Props) {
  const toggle = (u: string) => () => {
    const i = selected.indexOf(u)
    if (i === -1) onChange([...selected, u])
    else onChange(selected.filter(x => x !== u))
  }
  return (
    <List dense subheader={<ListSubheader>Меры</ListSubheader>} sx={{ maxHeight: 320, overflowY: 'auto', border: '1px solid #eee' }}>
      {measures.map(m => (
        <ListItemButton key={m.measure_unique_name} onClick={toggle(m.measure_unique_name)}>
          <FormControlLabel control={<Checkbox checked={selected.includes(m.measure_unique_name)} />} label={m.measure_name} />
        </ListItemButton>
      ))}
    </List>
  )
}
