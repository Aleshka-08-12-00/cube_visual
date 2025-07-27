import { useState } from 'react'
import { Box, Divider, Stack } from '@mui/material'
import QueryBuilder from '../components/QueryBuilder'
import ResultsTable from '../components/ResultsTable'
import ChartView from '../components/ChartView'
import 'react-pivottable/pivottable.css'
import { QueryRunResponse } from '../types'
import PivotTableUI from 'react-pivottable/PivotTableUI'
import createPlotlyRenderers from 'react-pivottable/PlotlyRenderers'
import Plot from 'react-plotly.js'

const PlotlyRenderers = createPlotlyRenderers(Plot as any)

export default function Explorer() {
  const [result, setResult] = useState<QueryRunResponse | null>(null)
  const [pivotState, setPivotState] = useState<any>({})
  const data = result ? [result.columns, ...result.rows] : [[]]
  return (
    <Stack gap={3}>
      <QueryBuilder onResult={setResult} />
      <Divider />
      <ResultsTable result={result} />
      <Divider />
      <ChartView result={result} />
      <Divider />
      <Box>
        <PivotTableUI data={data} onChange={s => setPivotState(s)} renderers={PlotlyRenderers} {...pivotState} />
      </Box>
    </Stack>
  )
}
