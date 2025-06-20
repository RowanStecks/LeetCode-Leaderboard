import requests
import json
import time
from info import USERNAMES, country_flags, languageLinks
from datetime import datetime

URL = "https://leetcode.com/graphql"
HEADERS = {
    "Content-Type": "application/json",
}

QUERY = """
query userProfile($username: String!) {
  matchedUser(username: $username) {
    username
    profile {
      ranking
      userAvatar
      realName
      school
      countryName
      company
    }
    submitStats {
      totalSubmissionNum {
        difficulty
        count
        submissions
      }
      acSubmissionNum {
        difficulty
        count
        submissions
      }
    }
  }
  userContestRanking(username: $username) {
    attendedContestsCount
    rating
    globalRanking
    badge {
      name
    }
  }
  matchedUser(username: $username) {
    languageProblemCount {
      languageName
      problemsSolved
    }
  }
  matchedUser(username: $username) {
    badges {
      name
    }
  }
}
"""

QUERY2 = """
query userProfileCalendar($username: String!, $year: Int) {
  matchedUser(username: $username) {
    userCalendar(year: $year) {
      activeYears
      submissionCalendar
    }
  }
}
"""


def getCountryCode(country):
    return country_flags.get(country, "")

def getLanguagePNG(language):
    return languageLinks.get(language, "")


def test(username, year):
    response = requests.post(
        URL,
        headers=HEADERS,
        json={
            "query": QUERY2,
            "variables": {"username": username, "year": year}
        }
    )
    data = response.json()
    user = data.get("data", {}).get("matchedUser")
    if user == None:
        return {}
    parsedString = json.loads(user.get("userCalendar").get("submissionCalendar"))
    return parsedString


def fetch_user_data(username):
    response = requests.post(
        URL,
        headers=HEADERS,
        json={
            "query": QUERY,
            "variables": {"username": username}
        }
    )
    data = response.json()

    user = data.get("data", {}).get("matchedUser")
    contestStats = data.get("data", {}).get("userContestRanking")
    languageStats = data.get("data", {}).get("matchedUser")
    badgeStats = data.get("data", {}).get("matchedUser")

    company = ""
    school = ""
    countryName = ""
    if user.get("profile").get("company") != None:
        company = user.get("profile").get("company")
    if user.get("profile").get("school") != None:
        school = user.get("profile").get("school")
    if user.get("profile").get("countryName") != None:
        countryName = user.get("profile").get("countryName")

    submissionDict = {}
    submissionsPerYear = []
    for y in range(2013, 2026):
        currYear = test(username, y)
        submissionDict.update(currYear)
        if len(currYear) != 0:
            if y % 4 == 0:
                submissionsPerYear.append(f"{y}: {len(currYear)}/366 - {sum(currYear.values())}")
            else:
                submissionsPerYear.append(f"{y}: {len(currYear)}/365 - {sum(currYear.values())}")
    submissionDays = len(submissionDict)
    
    maxStreak = 0
    currentStreak = 0
    currentStreakDates = []
    longestStreakDates = []
    if len(submissionDict) != 0:
      timestamps = sorted(map(int, submissionDict.keys()))

      longest_streak = []
      current_streak = [timestamps[0]]

      for i in range(1, len(timestamps)):
          if timestamps[i] == timestamps[i - 1] + 86400:
              current_streak.append(timestamps[i])
          else:
              if len(current_streak) > len(longest_streak):
                  longest_streak = current_streak
              current_streak = [timestamps[i]]

      # Check the last streak
      if len(current_streak) > len(longest_streak):
          longest_streak = current_streak

      currentStreak = len(current_streak)
      maxStreak = len(longest_streak)

      currentStreakDates = [(datetime.fromtimestamp(current_streak[0])).strftime("%b %d, %Y"), (datetime.fromtimestamp(current_streak[-1])).strftime("%b %d, %Y")]
      longestStreakDates = [(datetime.fromtimestamp(longest_streak[0])).strftime("%b %d, %Y"), (datetime.fromtimestamp(longest_streak[-1])).strftime("%b %d, %Y")]

    daysBadge = "None"
    badgeCategories = [0, 0, 0, 0, 0]
    for x in badgeStats.get("badges"):
            if x.get("name") == "Daily Coding Challenge":
                badgeCategories[3] += 1
            elif x.get("name") == "Study Plan Award" or x.get("name") == "Study Plan V2 Award":
                badgeCategories[4] += 1
            elif x.get("name") == "Annual Badge":
                badgeCategories[2] += 1
            elif x.get("name") == "Guardian" or x.get("name") == "Knight":
                badgeCategories[0] = 1         

            if x.get("name") == "Submission Badge":
                badgeCategories[1] += 1
                if badgeCategories[1] == 1:
                    daysBadge = "https://assets.leetcode.com/static_assets/marketing/lg365.png"
                elif badgeCategories[1] == 2:
                    daysBadge = "https://assets.leetcode.com/static_assets/marketing/lg500.png"
                elif badgeCategories[1] == 3:
                    daysBadge = "https://assets.leetcode.com/static_assets/marketing/lg1k.png"   
                elif badgeCategories[1] == 4:
                    daysBadge = "https://assets.leetcode.com/static_assets/marketing/lg2k.png"                                              
    
    primaryLanguage = max(languageStats.get("languageProblemCount"), key=lambda x: x["problemsSolved"])

    if user and contestStats: # if has participated in a contest
        profile = user.get("profile", {})
        if not contestStats.get("badge"): # if doesn't have a contest badge
            return {
                "username": user.get("username"),
                "ranking": profile.get("ranking"),
                "userAvatar": profile.get("userAvatar"),
                "realName": profile.get("realName"),
                "school": school,
                "countryName": countryName,
                "countryCodePNG": f"https://raw.githubusercontent.com/RowanStecks/leetcode-leaderboard/3ced7c32c37e9730aeed879ac62a70bfdf33c160/flags/4x3/{getCountryCode(countryName)}",
                "company": company,
                "globalRanking": contestStats.get("globalRanking"),
                "rating": round(contestStats.get("rating")),
                "attendedContestsCount": contestStats.get("attendedContestsCount"),
                "badge": "None",
                "badgePNG": "None",
                "primaryLanguage": primaryLanguage["languageName"],
                "primaryLanguagePNG": getLanguagePNG(primaryLanguage["languageName"]),
                "primaryLanguageCount": primaryLanguage["problemsSolved"],
                "totalProblemsSolved": user.get("submitStats").get("acSubmissionNum")[0].get("count"),
                "easySolved": user.get("submitStats").get("acSubmissionNum")[1].get("count"),
                "mediumSolved": user.get("submitStats").get("acSubmissionNum")[2].get("count"),
                "hardSolved": user.get("submitStats").get("acSubmissionNum")[3].get("count"),
                "badgeCount": len(badgeStats.get("badges")),
                "daysBadgeCount": daysBadge,
                "badgeCategories": badgeCategories,
                "submissions": user.get("submitStats").get("totalSubmissionNum")[0].get("submissions"),
                "acceptanceRate": round(((user.get("submitStats").get("acSubmissionNum")[0].get("submissions") / user.get("submitStats").get("totalSubmissionNum")[0].get("submissions")) * 100), 2),
                "submissionDays": submissionDays,
                "submissionsPerYear": submissionsPerYear,
                "maxStreak": maxStreak,
                "currentStreak": currentStreak,
                "currentStreakDates": currentStreakDates,
                "longestStreakDates": longestStreakDates,
            }
        else: # if has a contest badge
            return {
                "username": user.get("username"),
                "ranking": profile.get("ranking"),
                "userAvatar": profile.get("userAvatar"),
                "realName": profile.get("realName"),
                "school": school,
                "countryName": countryName,
                "countryCodePNG": f"https://raw.githubusercontent.com/RowanStecks/leetcode-leaderboard/3ced7c32c37e9730aeed879ac62a70bfdf33c160/flags/4x3/{getCountryCode(countryName)}",
                "company": company,
                "globalRanking": contestStats.get("globalRanking"),
                "rating": round(contestStats.get("rating")),
                "attendedContestsCount": contestStats.get("attendedContestsCount"),
                "badge": contestStats.get("badge").get("name"),
                "badgePNG": f"https://leetcode.com/static/images/badges/{contestStats.get("badge").get("name").lower()}.png",
                "primaryLanguage": primaryLanguage["languageName"],
                "primaryLanguagePNG": getLanguagePNG(primaryLanguage["languageName"]),
                "primaryLanguageCount": primaryLanguage["problemsSolved"],
                "totalProblemsSolved": user.get("submitStats").get("acSubmissionNum")[0].get("count"),
                "easySolved": user.get("submitStats").get("acSubmissionNum")[1].get("count"),
                "mediumSolved": user.get("submitStats").get("acSubmissionNum")[2].get("count"),
                "hardSolved": user.get("submitStats").get("acSubmissionNum")[3].get("count"),
                "badgeCount": len(badgeStats.get("badges")),
                "daysBadgeCount": daysBadge,
                "badgeCategories": badgeCategories,
                "submissions": user.get("submitStats").get("totalSubmissionNum")[0].get("submissions"),
                "acceptanceRate": round(((user.get("submitStats").get("acSubmissionNum")[0].get("submissions") / user.get("submitStats").get("totalSubmissionNum")[0].get("submissions")) * 100), 2),
                "submissionDays": submissionDays,
                "submissionsPerYear": submissionsPerYear,
                "maxStreak": maxStreak,
                "currentStreak": currentStreak,
                "currentStreakDates": currentStreakDates,
                "longestStreakDates": longestStreakDates,
            }
    elif user: # if hasn't participated in a contest (unrated)
        profile = user.get("profile", {})
        return {
            "username": user.get("username"),
            "ranking": profile.get("ranking"),
            "userAvatar": profile.get("userAvatar"),
            "realName": profile.get("realName"),
            "school": school,
            "countryName": countryName,
            "countryCodePNG": f"https://raw.githubusercontent.com/RowanStecks/leetcode-leaderboard/3ced7c32c37e9730aeed879ac62a70bfdf33c160/flags/4x3/{getCountryCode(countryName)}",
            "company": company,
            "globalRanking": -1,
            "rating": -1,
            "attendedContestsCount": 0,
            "badge": "None",
            "badgePNG": "None",
            "primaryLanguage": primaryLanguage["languageName"],
            "primaryLanguagePNG": getLanguagePNG(primaryLanguage["languageName"]),
            "primaryLanguageCount": primaryLanguage["problemsSolved"],
            "totalProblemsSolved": user.get("submitStats").get("acSubmissionNum")[0].get("count"),
            "easySolved": user.get("submitStats").get("acSubmissionNum")[1].get("count"),
            "mediumSolved": user.get("submitStats").get("acSubmissionNum")[2].get("count"),
            "hardSolved": user.get("submitStats").get("acSubmissionNum")[3].get("count"),
            "badgeCount": len(badgeStats.get("badges")),
            "daysBadgeCount": daysBadge,
            "badgeCategories": badgeCategories,
            "submissions": user.get("submitStats").get("totalSubmissionNum")[0].get("submissions"),
            "acceptanceRate": round(((user.get("submitStats").get("acSubmissionNum")[0].get("submissions") / user.get("submitStats").get("totalSubmissionNum")[0].get("submissions")) * 100), 2),
            "submissionDays": submissionDays,
            "submissionsPerYear": submissionsPerYear,
            "maxStreak": maxStreak,
            "currentStreak": currentStreak,
            "currentStreakDates": currentStreakDates,
            "longestStreakDates": longestStreakDates,
        }
    else:
        return {"username": username, "error": "User not found"}

def main():

    try:
        with open('pydata.json', 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    for username in USERNAMES:
        print(f"Fetching {username}...")
        user_data = fetch_user_data(username)
        data["data"].append(user_data)
    with open('pydata.json', 'w') as f:
        json.dump(data, f, indent=4)
     
if __name__ == "__main__":
    main()
