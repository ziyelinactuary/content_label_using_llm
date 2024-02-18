class PromptBuilder(object):
    HUMAN_PROMPT = "\n\nHuman:"
    AI_PROMPT = "\n\nAssistant:"

    @staticmethod
    def build_xml_one_title(input_df, index: int):
        return "<title><id>" + input_df.asin[index]+"</id><content_summary>" + input_df.synopsis[index] + " " + str(input_df.plot_outline[index]) + "</content_summary></title>"

    @staticmethod
    def build_prompt_string(startIndex, endIndex, content_metadata):
        request_body = ""
        for i in range(startIndex, endIndex):
            request_body = request_body + PromptBuilder.build_xml_one_title(content_metadata, i)+"\n"
        prompt_parts = [
            f"""{PromptBuilder.HUMAN_PROMPT}Determine if the title contains violence content based on content summary
    Each title document contains the following information enclosed in XML tags:
    - id: a unique identifier for the title
    - conent_summary: content summary of the title
     
    Example_1 input:
    <request>
        <title><id>78X8J0</id><content_summary>The film depicted Adolf Hitler's rise to power in Germany starting from his early days as a member of the Nazi party through his election as Chancellor in 1933. It showed his consolidation of power as he transformed the government into a one-party Nazi state and utilized propaganda to influence the public. The film then shifted to the later 1930s and the 1940s as the regime began invading neighboring countries, which eventually led to Germany's involvement in World War II. As the war turned against Germany, the film culminated with the defeat of Nazi Germany, Hitler's suicide, and the downfall and surrender of the Nazi government in 1945, ending Germany's fascist rule.</content_summary><title>
        <title><id>NU677P</id><content_summary>Lunch Money is going through an internal struggle to come to terms with difficult parts of his past that are still affecting him. He sees getting into the music business as a way to move forward, but his friend Stone disagrees and thinks it's unrealistic. While Stone believes they should focus on reliable work that pays well in the present, Lunch Money is convinced that becoming a rapper, despite potential perceptions of it being "fake", is a big opportunity for their financial future. Meanwhile, on a separate storyline, the mining equipment Claudia and Robin designed and built is facing mechanical problems as they do test runs transporting it through harsh terrain to set it up at the remote Wolverine mine site.</content_summary><title>
        <title><id>8J0K30</id><content_summary>Xena recruits four infamous criminals to help her steal back the secret to an impervious metal that the god of war Ares has acquired and is using to ensure victory in conflicts across Greece. The metal cannot be broken or damaged and gives Ares an unstoppable advantage on the battlefield. Knowing that entire cities will be destroyed if Ares continues to possess this metal, Xena must rely on the skills of these untrustworthy thieves, smugglers and mercenaries to break into Ares' heavily fortified stronghold and extract the information needed to defeat the metal. It will take all of Xena's cunning and leadership, as well as the criminals' unique talents, for them to successfully carry out this dangerous heist and save innocent lives from Ares' insatiable thirst for conflict and bloodshed.</content_summary><title>
        <title><id>WU88O3</id><content_summary>Tom confides in Diana that he is feeling lonely and suggests that they move in together romantically by "shacking up". However, Diana is not interested in pursuing a romantic relationship with Tom. Rather than reject him outright or have an uncomfortable conversation, her immediate reaction is to create physical distance and boundaries between them by building a partition to separate their living quarters. This subtly communicates her desire to keep their relationship professional without friendship, while avoiding a direct confrontation over his suggestion which could make things awkward ongoing. The partition allows each to have their own private space and maintains a clear line between them.</content_summary><title>
    </request>
    
    Example_1 output:
    <response>
        <li><id>78X8J0</id><cv>True</cv></li>
        <li><id>NU677P</id><cv>True</cv></li>
        <li><id>8J0K30</id><cv>False</cv></li>
        <li><id>WU88O3</id><cv>False</cv></li>
    </response>
    
    Example_2 input:
    <request>
        <title><id>13X890</id><content_summary>Jack Carter's son returns to the small town of Eureka after being gone for some time. However, his return begins to cause problems both in the town and personally for Carter. While his intentions may not be entirely clear at first, it seems his reappearance stirs up old feelings in Carter's daughter Allison that begin to affect her relationship with her father. Meanwhile, the Special Response Unit (SRU) team led by Carter faces a high-stakes operation involving an informant that has uncovered dangerous information. However, when this informant suddenly finds themselves embroiled in a messy love triangle that takes a deadly turn involving murder and betrayal, it threatens to compromise the SRU's mission and endanger everyone involved.</content_summary><title>
        <title><id>1367NP</id><content_summary>Lunch Money is going through an internal struggle to come to terms with difficult parts of his past that are still affecting him. He sees getting into the music business as a way to move forward, but his friend Stone disagrees and thinks it's unrealistic. While Stone believes they should focus on reliable work that pays well in the present, Lunch Money is convinced that becoming a rapper, despite potential perceptions of it being "fake", is a big opportunity for their financial future. Meanwhile, on a separate storyline, the mining equipment Claudia and Robin designed and built is facing mechanical problems as they do test runs transporting it through harsh terrain to set it up at the remote Wolverine mine site.</content_summary><title>
        <title><id>MM8930</id><content_summary>June uncovers an old scrapbook from their attic that triggers fond memories and nostalgia for the entire family. Ward and the boys gather around as June shares the scrapbook, flipping through the pages filled with photos documenting past family adventures, milestones, and other memorable moments they had experienced together over the years. With smiles and laughter, they reminisce about the joyous times captured in the snapshots, remembering meaningful details and inside jokes from years past as the scrapbook's pages transport them down memory lane, bringing the family even closer through their shared recollections of old times.</content_summary><title>
        <title><id>983340</id><content_summary>The Platonians onboard use their psychokinetic powers to manipulate and play tricks on the crew of the ship. Meanwhile, Jack helps set up Will and Grace with their first house flipping client named Zandra. However, Lorraine intentionally interferes with and causes issues for Karen and her husband Lyle as they try to work with her. The disparate storylines involve supernatural abilities disrupting ones tasks and relationships, while well-meaning connections are challenged by interpersonal friction and meddling.</content_summary><title>
    </request>
    
    Example_2 output:
    <response>
        <li><id>13X890</id><cv>True</cv></li>
        <li><id>1367NP</id><cv>True</cv></li>
        <li><id>MM8930</id><cv>False</cv></li>
        <li><id>983340</id><cv>False</cv></li>
    </response>
    
    Here is the new input:
    <request>
    {request_body}
    </request>
    What is the output? It is absolutely necessary that you only return a response enclosed by <response></response>. Make sure each requested title has an answer
    {PromptBuilder.AI_PROMPT}""",
        ]
        prompt = "\n".join(prompt_parts)
        return prompt
    