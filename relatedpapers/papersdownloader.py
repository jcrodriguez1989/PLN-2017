from collections import defaultdict
from xml.dom import minidom
import urllib.request
import os

from relatedpapers.paper import Paper
import relatedpapers.utils as ut

class PapersDownloader:

    def __init__(self, queries, papers_dir=None):
        """
        Downloads scientific papers from PubMedCentral according to a query.
        queries -- List of concepts to query.
        papers_dir -- Path of the local directory to store papers.
        """
        assert papers_dir is None or os.path.exists(papers_dir)
        query = 'AND'.join(queries)
        query = urllib.parse.quote_plus(query)
        self.query = query
        self.papers = defaultdict(str) # {paper_id -> Paper}
        self.papers_dir = papers_dir

    def get_paper_ids(self):
        """
        Gets the IDs of the papers according to the query, from PubMedCentral.
        """
        assert self.query != ""
        query = self.query
        query_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"  # ncbi api
        database = "pmc"  # PubMed Central papers

        complete_url = query_url + "esearch.fcgi?db=" + database + "&term=" + query
        complete_url += "&retmax=999999"
        xml_str = urllib.request.urlopen(complete_url).read()
        xml_doc = minidom.parseString(xml_str)
        ids = xml_doc.getElementsByTagName('Id')
        ids = [id.childNodes[0].data for id in ids]
        papers = defaultdict(str)
        for id in ids:
            papers[id] = None
        self.papers = dict(papers)
        print(len(ids), "papers to download.")
        return len(ids)

    def set_paper_ids(self, ids):
        """
        Manually set the IDs of the papers.
        ids -- Papers ids.
        """
        assert len(ids) > 0
        papers = defaultdict(str)
        for id in ids:
            papers[id] = None
        self.papers = dict(papers)

    def get_papers(self, n=float('inf')):
        """
        Get the first n downloaded papers.
        n -- Number of papers to download.
        """
        act_papers = [p for p in self.papers.values() if not p is None]
        n = min(len(act_papers), n)
        return act_papers[:n]

    def download_papers(self, n=float('inf')):
        """
        Downloads the first n queried papers.
        n -- Number of papers to download.
        """
        act_papers = self.papers
        ids = list(act_papers.keys())
        n = min(len(ids), n)
        for i in range(0, n):
            if act_papers[ids[i]] is None:
                act_paper = self.__download_paper(ids[i])
                act_papers[ids[i]] = act_paper
            ut.progress('Downloaded: {:2.0f} of {:2.0f}'.format(i+1, n))
        print('')
        self.papers = act_papers

    def __download_paper(self, paper_id):
        """
        Downloads a single paper.
        paper_id -- PMC paper id
        """
        path = str(self.papers_dir) + paper_id + '.xml'

        if (not self.papers_dir is None) and os.path.exists(path):
            xml_doc = minidom.parse(path)
        else:
            download_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
            database = 'pmc'
            download_url = download_url+'efetch.fcgi?db='+database+'&id='+paper_id
            xml_str = urllib.request.urlopen(download_url).read()
            xml_doc = minidom.parseString(xml_str)
            if (not self.papers_dir is None):
                f = open(path, 'w')
                xml_doc.writexml(f)
                f.close()

        title = ''
        title_x = xml_doc.getElementsByTagName('article-title')
        if (len(title_x) > 0):
            title = self.__get_text(title_x[0].childNodes)

        date = '0 0 0000'
        date_x = xml_doc.getElementsByTagName('pub-date')
        if (len(date_x) > 0):
            date = self.__get_text(date_x[0].childNodes)

        abstract = ''
        abstract_x = xml_doc.getElementsByTagName('abstract')
        if (len(abstract_x) > 0):
            abstract = self.__get_text(abstract_x[0].childNodes)

        body = ''
        body_x = xml_doc.getElementsByTagName('body')
        if (len(body_x) > 0):
            body = self.__get_text(body_x[0].childNodes)

        return Paper(paper_id, title, date, abstract, body)

    def __get_text(self, nodelist):
        """
        Gets all text from a nodelist object
        nodelist -- nodelist object to get the text
        """
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
            else:
                rc.append(self.__get_text(node.childNodes))
        return ' '.join(rc)

