import {
  Box,
  Breadcrumbs,
  Typography,
  Stack,
} from '@mui/material';
import ExtendedContentTable from '../../components/ExtendedContentTable';
import { TableDocument } from 'iconsax-react';
import NavigateNextIcon from '@mui/icons-material/NavigateNext'
import { Link, useLoaderData } from 'react-router-dom';
import { ExtractionGraph, Extractor, IndexifyClient } from 'getindexify';
import { mapExtractionPoliciesToRows } from '../../utils/helpers';
import ExtractorGraphTable from './ExtractorGraphTable';
import { IHash } from '../../types';
import CopyText from '../../components/CopyText';

const IndividualExtractionGraphPage = () => {
  const { 
    tasks,
    extractors,
    extractionGraph,
    client,
    namespace,
    extractorName
   } =
    useLoaderData() as {
      tasks: IHash,
      extractors: Extractor[],
      extractionGraph: ExtractionGraph
      client: IndexifyClient
      namespace: string
      extractorName: string
    }

  const extractionGraphString = JSON.parse(JSON.stringify(extractionGraph));
  const extractorString = JSON.parse(JSON.stringify(extractors));  
  const mappedRows = mapExtractionPoliciesToRows(extractionGraphString, extractorString, extractorName, tasks);

  return (
    <Stack direction="column" spacing={3}>
      <Breadcrumbs
        aria-label="breadcrumb"
        separator={<NavigateNextIcon fontSize="small" />}
      >
        <Typography color="text.primary">{namespace}</Typography>
        <Link color="inherit" to={`/${namespace}/extraction-graphs`}>
          <Typography color="text.primary">Extraction Graphs</Typography>
        </Link>
        <Typography color="text.primary">{extractorName}</Typography>
      </Breadcrumbs>
      <Box sx={{ p: 0 }}>
        <Box sx={{ mb: 3 }}>
          <div className="content-table-header">
            <div className="heading-icon-container">
              <TableDocument size="25" className="heading-icons" variant="Outline"/>
            </div>
            <Typography variant="h4" display={'flex'} flexDirection={'row'}>
              {extractorName} <CopyText text={extractorName} />
            </Typography>
          </div>
          <ExtractorGraphTable rows={mappedRows} graphName={extractorName} />
        </Box>
        <ExtendedContentTable
            client={client}
            extractionGraph={extractionGraph}
            graphName={extractorName}
            namespace={namespace}
          />
      </Box>
    </Stack>
  );
};

export default IndividualExtractionGraphPage;
