from drf_spectacular.utils import OpenApiExample

SURVEY_LIST_EXAMPLES = [
    OpenApiExample(
        name="Success example (200)",
        response_only=True,
        value={
          "surveys": [
            {
              "id": 1,
              "content": "깻잎 논쟁 당신의 선택은?",
              "createdAt": "2022-06-23 13:31:14",
              "deadline": None,
              "repliedItem": None,
              "items": [
                {
                  "id": 1,
                  "content": "완전 반대 ㅡㅡ"
                },
                {
                  "id": 2,
                  "content": "아무렴 어때?"
                }
              ]
            },
            {
              "id": 2,
              "content": "새우 논쟁 당신의 선택은?",
              "createdAt": "2022-06-23 13:32:01",
              "deadline": None,
              "repliedItem": None,
              "items": [
                {
                  "id": 3,
                  "content": "그럴 수도 있지"
                },
                {
                  "id": 4,
                  "content": "죽인다"
                },
                {
                  "id": 5,
                  "content": "왜 안 도와줌?"
                }
              ]
            }
          ]
        }
    )
]
