import { useEffect, useState } from 'react'
import { Accordion, AccordionDetails, AccordionSummary, Checkbox, Chip, CircularProgress, FormControlLabel, Stack, Typography } from '@mui/material'
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'
import { api } from '../api/client'
import { Dimension, Hierarchy } from '../types'

type Props = { cube: string; selectedHierarchies: string[]; onChange: (next: string[]) => void; title: string }
export default function DimensionTree({ cube, selectedHierarchies, onChange, title }: Props) {
  const [dims, setDims] = useState<Dimension[]>([])
  const [hmap, setHmap] = useState<Record<string, Hierarchy[]>>({})
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!cube) return
    setLoading(true)
    api.get<Dimension[]>('/schema/dimensions', { params: { cube } }).then(r => setDims(r.data)).finally(() => setLoading(false))
  }, [cube])

  const loadHs = async (d: string) => {
    if (hmap[d]) return
    const r = await api.get<Hierarchy[]>('/schema/hierarchies', { params: { cube, dimension_unique_name: d } })
    setHmap(p => ({ ...p, [d]: r.data }))
  }

  const toggleH = (h: string) => {
    if (selectedHierarchies.includes(h)) onChange(selectedHierarchies.filter(x => x !== h))
    else onChange([...selectedHierarchies, h])
  }

  return (
    <Stack gap={1}>
      <Typography variant="subtitle1">{title}</Typography>
      {loading && <CircularProgress size={18} />}
      {dims.map(d => (
        <Accordion key={d.dimension_unique_name} onChange={(_, ex) => ex && loadHs(d.dimension_unique_name)}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>{d.dimension_name}</AccordionSummary>
          <AccordionDetails>
            <Stack gap={1} direction="row" flexWrap="wrap">
              {(hmap[d.dimension_unique_name] || []).map(h => (
                <Chip
                  key={h.hierarchy_unique_name}
                  onClick={() => toggleH(h.hierarchy_unique_name)}
                  color={selectedHierarchies.includes(h.hierarchy_unique_name) ? 'primary' : 'default'}
                  variant={selectedHierarchies.includes(h.hierarchy_unique_name) ? 'filled' : 'outlined'}
                  label={h.hierarchy_name}
                />
              ))}
            </Stack>
          </AccordionDetails>
        </Accordion>
      ))}
      <FormControlLabel control={<Checkbox checked disabled />} label="Все члены выбранных иерархий" />
    </Stack>
  )
}
