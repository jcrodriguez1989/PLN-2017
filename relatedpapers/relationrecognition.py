class RelationRecognition:

    def __init__(self, papers, entities):
        """
        papers -- list of Papers to search for relational sents.
        entities -- list of lists, where each list is an entity, and each sublist possible synonyms of it.
        """
        #assert len(papers) > 0
        assert len(entities) > 0

        entities.sort(key=lambda x: len(x)) # for performance
        #self.papers = papers
        self.entities = entities
        self.related_papers = []

        for paper in papers:
            if self.__is_related(paper):
                print('Related paper!!')
                print(paper.id, paper.title)
        self.related_papers.sort(key=lambda x: len(x[1]), reverse=True)

    def __is_related(self, paper):
        entities = self.entities
        related_sents = []
        for sent in paper.get_full_paper():
            sent = sent.lower()
            is_related = True
            for entity in entities:
                any_related = False
                for sinom in entity:
                    any_related = any_related or sinom.lower() in sent
                    if any_related:
                        break
                is_related = is_related and any_related
                if not is_related:
                    break
            if is_related:
                related_sents.append(sent)
        if len(related_sents) > 0:
            self.related_papers.append((paper, related_sents))
        return len(related_sents) > 0

