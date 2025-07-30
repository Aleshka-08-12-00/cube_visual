import { useEffect, useMemo, useState } from 'react'
import { List, ListItem, ListItemText, MenuItem, Select, Stack, TextField } from '@mui/material'
import { api } from '../api/client'
import { Measure, Hierarchy } from '../types'

export type Zone = '' | 'row' | 'column' | 'value' | 'filter'
export type FieldAssignments = { rows: string[]; columns: string[]; values: string[]; filters: string[] }

interface Field {
  name: string
  unique_name: string
  type: 'measure' | 'hierarchy'
  zone: Zone
}

interface Props {
  cube: string
  onChange: (a: FieldAssignments) => void
}

export default function FieldList({ cube, onChange }: Props) {
  const [fields, setFields] = useState<Field[]>([])
  const [search, setSearch] = useState('')

  useEffect(() => {
    if (!cube) return
    Promise.all([
      api.get<Measure[]>('/schema/measures', { params: { cube } }),
      api.get<Hierarchy[]>('/schema/hierarchies', { params: { cube } })
    ]).then(([mRes, hRes]) => {
      setFields([
        ...mRes.data.map(m => ({ name: m.measure_name, unique_name: m.measure_unique_name, type: 'measure', zone: '' as Zone })),
        ...hRes.data.map(h => ({ name: h.hierarchy_name, unique_name: h.hierarchy_unique_name, type: 'hierarchy', zone: '' as Zone }))
      ])
    })
  }, [cube])

  useEffect(() => {
    const rows = fields.filter(f => f.zone === 'row').map(f => f.unique_name)
    const columns = fields.filter(f => f.zone === 'column').map(f => f.unique_name)
    const values = fields.filter(f => f.zone === 'value').map(f => f.unique_name)
    const filters = fields.filter(f => f.zone === 'filter').map(f => f.unique_name)
    onChange({ rows, columns, values, filters })
  }, [fields, onChange])

  const updateZone = (u: string, zone: Zone) => {
    setFields(f => f.map(fl => (fl.unique_name === u ? { ...fl, zone } : fl)))
  }

  const filtered = useMemo(
    () => fields.filter(f => f.name.toLowerCase().includes(search.toLowerCase())),
    [fields, search]
  )

  return (
    <Stack>
      <TextField size="small" label="Поиск" value={search} onChange={e => setSearch(e.target.value)} sx={{ mb: 1 }} />
      <List dense sx={{ maxHeight: 320, overflowY: 'auto', border: '1px solid #eee' }}>
        {filtered.map(f => (
          <ListItem key={f.unique_name} secondaryAction={
            <Select size="small" value={f.zone} onChange={e => updateZone(f.unique_name, e.target.value as Zone)} sx={{ minWidth: 120 }}>
              <MenuItem value="">-</MenuItem>
              <MenuItem value="filter">Фильтр</MenuItem>
              <MenuItem value="column">Колонка</MenuItem>
              <MenuItem value="row">Строка</MenuItem>
              <MenuItem value="value">Значение</MenuItem>
            </Select>
          }>
            <ListItemText primary={f.name} secondary={f.type === 'measure' ? 'Мера' : 'Измерение'} />
          </ListItem>
        ))}
      </List>
    </Stack>
  )
}
