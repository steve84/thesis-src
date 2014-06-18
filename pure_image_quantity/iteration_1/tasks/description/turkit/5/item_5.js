
var text = ""

for (var i = 0; i < 3; i++) {
    // improve text
    var hitId = createImproveHIT(text, 0.2, i)
    var hit = mturk.waitForHIT(hitId)
    
    var newText = hit.assignments[0].answer.newText
    print("-------------------")
    print(newText)
    print("-------------------")
    
    // verify improvement
    if (vote(text, newText, 0.01, i)) {
        text = newText
        mturk.approveAssignment(hit.assignments[0])
        print("\nvote = keep\n")
    } else {
        mturk.approveAssignment(hit.assignments[0])
        print("\nvote = reject\n")
    }    
}

print("Final description: " + text)

function createRequirements() {
		var q = [];
		q.push({"QualificationTypeId": "00000000000000000071", "Comparator": "EqualTo", "LocaleValue": {"Country" : "US"}});
		
		return q;
}

function createImproveHIT(oldText, improveCost, cnt) {
    default xml namespace = "http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionForm.xsd";
		var length = "" + ((cnt + 1) * 40);
    var q = <QuestionForm>
        <Question>
            <QuestionIdentifier>newText</QuestionIdentifier>
            <IsRequired>true</IsRequired>
            <QuestionContent>
                <FormattedContent><![CDATA[
					All the workers who have done a similar task in the past are excluded from this HIT. If you find your worker ID in the following table, your work <b>will be rejected</b>.<br /><br /><table border="1"><tr><td>ANJRINRP821LY</td><td>A3J47737YMH6WK</td><td>A291KO368YRYCR</td><td>A3KUFIF1ULONV1</td><td>A3AJR1PM02424Y</td></tr><tr><td>A2SFEEI806WFP9</td><td>A2Y9ZNZ0F24GHB</td><td>A1IA4CST74I1Q8</td><td>A3JLB1N2CB27BZ</td><td>AJAOE1PSNKGUE</td></tr></table><hr /><table border="0"><tr><td><img src="http://pegasus84.noip.me/www/unibe/thesis/5/image_1.JPG" alt="Image 1" width="250" border="2"></img><br /><br /><a href="http://pegasus84.noip.me/www/unibe/thesis/5/image_1.JPG" target="_blank">Link to full size image 1 (new window)</a></td><td><img src="http://pegasus84.noip.me/www/unibe/thesis/5/image_2.JPG" alt="Image 2" width="250" border="2"></img><br /><br /><a href="http://pegasus84.noip.me/www/unibe/thesis/5/image_2.JPG" target="_blank">Link to full size image 2 (new window)</a></td><td><img src="http://pegasus84.noip.me/www/unibe/thesis/5/image_3.JPG" alt="Image 3" width="250" border="2"></img><br /><br /><a href="http://pegasus84.noip.me/www/unibe/thesis/5/image_3.JPG" target="_blank">Link to full size image 3 (new window)</a></td><td><img src="http://pegasus84.noip.me/www/unibe/thesis/5/image_4.JPG" alt="Image 4" width="250" border="2"></img><br /><br /><a href="http://pegasus84.noip.me/www/unibe/thesis/5/image_4.JPG" target="_blank">Link to full size image 4 (new window)</a></td><td><img src="http://pegasus84.noip.me/www/unibe/thesis/5/image_5.JPG" alt="Image 5" width="250" border="2"></img><br /><br /><a href="http://pegasus84.noip.me/www/unibe/thesis/5/image_5.JPG" target="_blank">Link to full size image 5 (new window)</a></td></tr><tr><td><img src="http://pegasus84.noip.me/www/unibe/thesis/5/image_6.JPG" alt="Image 6" width="250" border="2"></img><br /><br /><a href="http://pegasus84.noip.me/www/unibe/thesis/5/image_6.JPG" target="_blank">Link to full size image 6 (new window)</a></td><td><img src="http://pegasus84.noip.me/www/unibe/thesis/5/image_7.JPG" alt="Image 7" width="250" border="2"></img><br /><br /><a href="http://pegasus84.noip.me/www/unibe/thesis/5/image_7.JPG" target="_blank">Link to full size image 7 (new window)</a></td><td><img src="http://pegasus84.noip.me/www/unibe/thesis/5/image_8.JPG" alt="Image 8" width="250" border="2"></img><br /><br /><a href="http://pegasus84.noip.me/www/unibe/thesis/5/image_8.JPG" target="_blank">Link to full size image 8 (new window)</a></td><td><img src="http://pegasus84.noip.me/www/unibe/thesis/5/image_9.JPG" alt="Image 9" width="250" border="2"></img><br /><br /><a href="http://pegasus84.noip.me/www/unibe/thesis/5/image_9.JPG" target="_blank">Link to full size image 9 (new window)</a></td><td></td></tr></table>
					The goal of the requester of the HIT is to generate eBay auctions by MTurk workers based on images of the item.<br /><br />
					<b>Instructions</b>: Improve and/or extend the description of the auction item(s) on the images. Keep in mind the following remarks:
					<ul>
					<li>If the description doesn't contain approximately <b>5 sentences</b> then try to add more text
					<ul>
						<li>Include specific information like size, shape, color, age, manufacture date, company/artist/author, and notable features or markings if possible</li>
						<li>Make the description as readable as possible</li>
						<li>Don't say anything that isn't true.</li>
						<li>Don't use all caps</li>
						<li>Don't include email addresses and some links</li>
					</ul>
					</li>
					<li>If the description is long enough then try to improve it</li>
					</ul>					
]]></FormattedContent>
            </QuestionContent>
            <AnswerSpecification>
                <FreeTextAnswer>
                    <Constraints>
                        <Length minLength={length} maxLength="5000"></Length>
                        <AnswerFormatRegex regex="\S" errorText="The description cannot be blank."/>
                    </Constraints>
                    <DefaultText>{oldText}</DefaultText>
                    <NumberOfLinesSuggestion>10</NumberOfLinesSuggestion>
                </FreeTextAnswer>
            </AnswerSpecification>
        </Question>
        <Question>
            <QuestionIdentifier>description_improve_feedback</QuestionIdentifier>
            <QuestionContent>
						<Title>Your personal feedback (optional)</Title>
                <FormattedContent><![CDATA[
				Give your personal feedback about the task. This <b>can</b> contain one of the following aspects:
        <ul>
        <li>Problems of the task (e.g. images are not visible)</li>
        <li>Instructions are not clear enough</li>
        </ul>
]]></FormattedContent>
            </QuestionContent>
            <AnswerSpecification>
                <FreeTextAnswer>
                    <NumberOfLinesSuggestion>3</NumberOfLinesSuggestion>
                </FreeTextAnswer>
            </AnswerSpecification>
        </Question>				
    </QuestionForm>
	
	// var html = '<ul>'
	// + '<li>Please improve the description for this image.</li>'
	// + '<li>People will vote whether to approve your work.</li>'
	// + '</ul>'
	// + '<img src="' + imgSrc + '" alt="description not available"></img>';
	// var content = '<![CDATA[' + html + ']]>';

    // var q = new XML('<QuestionForm><Question><QuestionIdentifier>newText</QuestionIdentifier><IsRequired>true</IsRequired><QuestionContent><FormattedContent>' + content + '</FormattedContent></QuestionContent><AnswerSpecification><FreeTextAnswer><Constraints><Length minLength="2" maxLength="500"></Length><AnswerFormatRegex regex="\S" errorText="The content cannot be blank."/></Constraints><DefaultText>' + oldText + '</DefaultText><NumberOfLinesSuggestion>3</NumberOfLinesSuggestion></FreeTextAnswer></AnswerSpecification></Question></QuestionForm>');
	
	return mturk.createHIT({title : "Improve/extend description of auction item(s) on pictures", desc : "Improve and/or extend the description of an auction item based on three images", question : "" + q, reward : improveCost, assignmentDurationInSeconds : 60 * 120, qualificationRequirements : createRequirements()})
}


function vote(textA, textB, voteCost, nbr) {
	if (nbr == 0) return true;
    default xml namespace = "http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionForm.xsd";
    var q = <QuestionForm>
        <Question>
            <QuestionIdentifier>vote</QuestionIdentifier>
            <IsRequired>true</IsRequired>
            <QuestionContent>
                <FormattedContent><![CDATA[
					All the workers who have done a similar task in the past are excluded from this HIT. If you find your worker ID in the following table, your work <b>will be rejected</b>.<br /><br /><table border="1"><tr><td>ANJRINRP821LY</td><td>A3J47737YMH6WK</td><td>A291KO368YRYCR</td><td>A3KUFIF1ULONV1</td><td>A3AJR1PM02424Y</td></tr><tr><td>A2SFEEI806WFP9</td><td>A2Y9ZNZ0F24GHB</td><td>A1IA4CST74I1Q8</td><td>A3JLB1N2CB27BZ</td><td>AJAOE1PSNKGUE</td></tr></table><hr /><table border="0"><tr><td><img src="http://pegasus84.noip.me/www/unibe/thesis/5/image_1.JPG" alt="Image 1" width="250" border="2"></img><br /><br /><a href="http://pegasus84.noip.me/www/unibe/thesis/5/image_1.JPG" target="_blank">Link to full size image 1 (new window)</a></td><td><img src="http://pegasus84.noip.me/www/unibe/thesis/5/image_2.JPG" alt="Image 2" width="250" border="2"></img><br /><br /><a href="http://pegasus84.noip.me/www/unibe/thesis/5/image_2.JPG" target="_blank">Link to full size image 2 (new window)</a></td><td><img src="http://pegasus84.noip.me/www/unibe/thesis/5/image_3.JPG" alt="Image 3" width="250" border="2"></img><br /><br /><a href="http://pegasus84.noip.me/www/unibe/thesis/5/image_3.JPG" target="_blank">Link to full size image 3 (new window)</a></td><td><img src="http://pegasus84.noip.me/www/unibe/thesis/5/image_4.JPG" alt="Image 4" width="250" border="2"></img><br /><br /><a href="http://pegasus84.noip.me/www/unibe/thesis/5/image_4.JPG" target="_blank">Link to full size image 4 (new window)</a></td><td><img src="http://pegasus84.noip.me/www/unibe/thesis/5/image_5.JPG" alt="Image 5" width="250" border="2"></img><br /><br /><a href="http://pegasus84.noip.me/www/unibe/thesis/5/image_5.JPG" target="_blank">Link to full size image 5 (new window)</a></td></tr><tr><td><img src="http://pegasus84.noip.me/www/unibe/thesis/5/image_6.JPG" alt="Image 6" width="250" border="2"></img><br /><br /><a href="http://pegasus84.noip.me/www/unibe/thesis/5/image_6.JPG" target="_blank">Link to full size image 6 (new window)</a></td><td><img src="http://pegasus84.noip.me/www/unibe/thesis/5/image_7.JPG" alt="Image 7" width="250" border="2"></img><br /><br /><a href="http://pegasus84.noip.me/www/unibe/thesis/5/image_7.JPG" target="_blank">Link to full size image 7 (new window)</a></td><td><img src="http://pegasus84.noip.me/www/unibe/thesis/5/image_8.JPG" alt="Image 8" width="250" border="2"></img><br /><br /><a href="http://pegasus84.noip.me/www/unibe/thesis/5/image_8.JPG" target="_blank">Link to full size image 8 (new window)</a></td><td><img src="http://pegasus84.noip.me/www/unibe/thesis/5/image_9.JPG" alt="Image 9" width="250" border="2"></img><br /><br /><a href="http://pegasus84.noip.me/www/unibe/thesis/5/image_9.JPG" target="_blank">Link to full size image 9 (new window)</a></td><td></td></tr></table>
					The goal of the requester of the HIT is to generate eBay auctions by MTurk workers based on images of the item.<br /><br />
					<b>Instructions:</b> Which description of the auction item(s) on the pictures is better? The following factors <b>can</b> affect your decision: 
					<ul>
						<li>One description is more informative than the other</li>
						<li>One description contains more information about the auction item then the other</li>
						<li>One description contains wrong information</li>
						<li>One description has spelling mistakes</li>
					</ul>				
]]></FormattedContent>
            </QuestionContent>
            <AnswerSpecification>
                <SelectionAnswer>
                    <Selections>
                    </Selections>
                </SelectionAnswer>
            </AnswerSpecification>
        </Question>
        <Question>
            <QuestionIdentifier>description_vote_feedback</QuestionIdentifier>
            <QuestionContent>
						<Title>Your personal feedback (optional)</Title>
                <FormattedContent><![CDATA[
				Give your personal feedback about the task. This <b>can</b> contain one of the following aspects:
        <ul>
        <li>Problems of the task (e.g. images are not visible)</li>
        <li>Instructions are not clear enough</li>
        </ul>
]]></FormattedContent>
            </QuestionContent>
            <AnswerSpecification>
                <FreeTextAnswer>
                    <NumberOfLinesSuggestion>3</NumberOfLinesSuggestion>
                </FreeTextAnswer>
            </AnswerSpecification>
        </Question>					
    </QuestionForm>

    var options = [{key:"a",value:textA}, {key:"b",value:textB}]
    shuffle(options)
    foreach(options, function (op) {
        default xml namespace = "http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionForm.xsd";
        q.Question.AnswerSpecification.SelectionAnswer.Selections.Selection +=
            <Selection>
                <SelectionIdentifier>{op.key}</SelectionIdentifier>
                <Text>{op.value}</Text>
            </Selection>
    })
    var voteHitId = mturk.createHIT({title : "Vote on auction item description improvements", desc : "Decide which auction item description is better/suitable for the item(s) on three pictures", question : "" + q,  reward : voteCost, assignmentDurationInSeconds : 60 * 30, maxAssignments : 2, qualificationRequirements : createRequirements()})
    var voteResults = mturk.vote(voteHitId, function (answer) {return answer.vote[0]})
    return voteResults.bestOption == "b"
}
